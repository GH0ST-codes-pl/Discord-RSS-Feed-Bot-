# Discord RSS Feed Bot 🚀

A robust and efficient Discord bot designed to automatically monitor RSS feeds and publish new updates directly to your Discord channels. Built with Python using `discord.py` and `feedparser`.

## ✨ Key Features
- **Real-time Monitoring**: Automatically checks for new RSS feed entries every 60 seconds (configurable).
- **Rich Embeds**: Posts updates using beautiful Discord Embeds including titles, descriptions, and links.
- **Media Detection**: Intelligent detection of images and video content (YouTube, Vimeo) for enhanced visual presentation.
- **Smart Tracking**: Remembers previously posted links in a `posted.json` file to prevent duplicate messages.
- **Multi-Feed Support**: Support for multiple RSS feeds, each targetable to specific Discord channels.
- **Auto-Cleanup**: Automatically manages the history of posted links to optimize performance.
- **Async Implementation**: Fully asynchronous operations to ensure high responsiveness.

## 📋 Prerequisites
- Python 3.8 or higher
- A Discord Bot Token (via [Discord Developer Portal](https://discord.com/developers/applications))
- Discord Channel IDs where you want to receive updates

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GH0ST-codes-pl/Discord-RSS-Feed-Bot-.git
   cd "BOT DO RSS FEEDÓW"
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install python-dotenv feedparser discord.py aiohttp
   ```

## ⚙️ Configuration

### 1. Environment Variables
Create a `.env` file in the root directory and add your Discord bot token:
```env
DISCORD_BOT_TOKEN=your_token_here
```

### 2. Feed Configuration
Edit the `feeds.json` file to include your RSS feeds and target channel IDs:
```json
{
    "https://example.com/rss": 1234567890,
    "https://another-site.com/feed": 9876543210
}
```
*Note: The key is the RSS feed URL, and the value is the numerical Discord Channel ID.*

## 🏁 Running the Bot

### Linux/Mac:
Using the provided start script:
```bash
chmod +x start_bot.sh
./start_bot.sh
```

### Manual execution:
```bash
# Linux/Mac
./venv/bin/python bot.py

# Windows
venv\Scripts\python bot.py
```

## 📂 Project Structure
- `bot.py`: Main application logic.
- `.env`: (Private) Contains your sensitive bot token.
- `feeds.json`: Configuration for your RSS feeds and target channels.
- `posted.json`: (Auto-generated) Database of already posted links.
- `bot.log`: (Auto-generated) Detailed logs of bot activity.
- `start_bot.sh`: Convenience script for Unix-based systems.

## 🛠️ Advanced Configuration
You can fine-tune the bot's behavior by modifying the constants in `bot.py`:
- `CHECK_INTERVAL`: Frequency of RSS checks (default: 60s).
- `MAX_DESCRIPTION_LENGTH`: Limit for message descriptions (default: 4096).
- `MAX_POSTED_LINKS`: History size for tracking (default: 1000).

## 🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author
Developed with the assistance of AI to empower the Discord community.
