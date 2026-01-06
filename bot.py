import discord
from discord.ext import tasks
import feedparser
import asyncio
import json
import os
import re
import logging
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime, timedelta
import time
from email.utils import parsedate_to_datetime
from dotenv import load_dotenv

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Wczytaj zmienne środowiskowe
load_dotenv()

# Konfiguracja
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Stałe konfiguracyjne
POSTED_FILE = "posted.json"
FEEDS_FILE = "feeds.json"
MAX_DESCRIPTION_LENGTH = 4096
MAX_POSTED_LINKS = 1000
CHECK_INTERVAL = 60
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
MAX_POSTS_PER_CYCLE = 0

# Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = discord.Client(intents=intents)

class RSSBot:
    def __init__(self):
        self.posted_links = self.load_posted_links()
        self.feeds = self.load_feeds()
        self.session = None
        self.last_cleanup = datetime.now()

    def load_feeds(self) -> Dict[str, int]:
        """Ładuje listę feedów z pliku JSON"""
        if os.path.exists(FEEDS_FILE):
            try:
                with open(FEEDS_FILE, "r", encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Błąd ładowania {FEEDS_FILE}: {e}")
        return {}

    def load_posted_links(self) -> Dict[str, List[str]]:
        """Ładuje listę opublikowanych linków"""
        if os.path.exists(POSTED_FILE):
            try:
                with open(POSTED_FILE, "r", encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Błąd ładowania {POSTED_FILE}: {e}")
        return {}

    def save_posted_links(self):
        """Zapisuje listę opublikowanych linków"""
        try:
            with open(POSTED_FILE, "w", encoding='utf-8') as f:
                json.dump(self.posted_links, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Błąd zapisu {POSTED_FILE}: {e}")

    def cleanup_posted_links(self):
        """Czyści stare linki"""
        for feed_url in self.posted_links:
            if len(self.posted_links[feed_url]) > MAX_POSTED_LINKS:
                self.posted_links[feed_url] = self.posted_links[feed_url][-MAX_POSTED_LINKS//2:]
                logger.info(f"Wyczyszczono stare linki dla: {feed_url}")

    def clean_html(self, text: str) -> str:
        """Proste usuwanie tagów HTML"""
        if not text:
            return ""
        clean = re.sub(r'<[^>]+>', '', text)
        return re.sub(r'\s+', ' ', clean).strip()

    def extract_image(self, entry) -> Optional[str]:
        """Próbuje znaleźć obrazek w entry"""
        # Sprawdzanie enclosures
        if hasattr(entry, 'enclosures'):
            for enc in entry.enclosures:
                if enc.get('type', '').startswith('image/'):
                    return enc.get('href')
        
        # Sprawdzanie media_content
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('type', '').startswith('image/') or media.get('medium') == 'image':
                    return media.get('url')
                    
        # Szukanie w description/summary tagu img
        summary = entry.get('summary', '') or entry.get('description', '')
        if summary:
            match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
            if match:
                return match.group(1)
                
        return None

    def extract_video(self, entry) -> Optional[str]:
        """Proste szukanie linku do wideo (YouTube, itp)"""
        content = str(entry)
        # Proste regexy dla popularnych serwisów
        patterns = [
            r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)',
            r'(https?://youtu\.be/[\w-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        return None

    async def fetch_feed(self, feed_url: str):
        """Pobiera feed"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        try:
            async with self.session.get(feed_url, timeout=REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    content = await response.text()
                    return feedparser.parse(content)
        except Exception as e:
            logger.error(f"Błąd pobierania {feed_url}: {e}")
        return None

    async def send_post(self, channel, entry, feed_url: str):
        """Wysyła post na Discorda"""
        title = entry.get('title', 'Nowy wpis')
        link = entry.get('link', '')
        summary = entry.get('summary', '') or entry.get('description', '')
        
        # Wideo ma priorytet (jeśli jest linkiem YT, wyślij jako wiadomość żeby był embed)
        video_url = self.extract_video(entry)
        
        embed = discord.Embed(
            title=title[:256],
            description=self.clean_html(summary)[:MAX_DESCRIPTION_LENGTH] or "...",
            url=link,
            color=discord.Color.blue()
        )
        
        # Obrazek w embedzie
        image_url = self.extract_image(entry)
        if image_url:
            embed.set_image(url=image_url)
            
        try:
            await channel.send(embed=embed)
            if video_url:
                await channel.send(f"Wideo: {video_url}")
                
            self.posted_links.setdefault(feed_url, []).append(link)
            logger.info(f"Wysłano: {title}")
        except Exception as e:
            logger.error(f"Błąd wysyłania: {e}")

    async def process_feeds(self):
        """Główna logika przetwarzania"""
        self.feeds = self.load_feeds() # Odśwież feedy (hot-reload listy)
        
        for feed_url, channel_id in self.feeds.items():
            try:
                channel = bot.get_channel(channel_id)
                if not channel:
                    logger.warning(f"Brak dostępu do kanału {channel_id}")
                    continue
                    
                feed = await self.fetch_feed(feed_url)
                if not feed or not hasattr(feed, 'entries'):
                    continue

                # Nowe posty (odwrócona kolejność - od najstarszego nieopublikowanego)
                for entry in reversed(feed.entries):
                    link = entry.get('link')
                    if not link or link in self.posted_links.get(feed_url, []):
                        continue
                        
                    await self.send_post(channel, entry, feed_url)
                    await asyncio.sleep(2) # Anti-spam
                    
                self.save_posted_links()
                
            except Exception as e:
                logger.error(f"Błąd feedu {feed_url}: {e}")

rss_bot = RSSBot()

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_feeds_loop():
    await rss_bot.process_feeds()

@check_feeds_loop.before_loop
async def before_check():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    logger.info(f"Zalogowano jako {bot.user}")
    check_feeds_loop.start()

if __name__ == "__main__":
    if TOKEN and TOKEN != "twoj_token_tutaj":
        try:
            bot.run(TOKEN)
        except Exception as e:
             logger.error(f"Błąd uruchamiania: {e}")
    else:
        logger.error("Brak poprawnego tokena w .env! Ustaw DISCORD_BOT_TOKEN.")
        print("CRITICAL: Brak poprawnego tokena w .env! Ustaw DISCORD_BOT_TOKEN.")
