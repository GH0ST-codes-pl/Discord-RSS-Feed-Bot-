# Discord RSS Bot

Bot Discord do automatycznego publikowania wpisów z feedów RSS na kanałach Discord.

## Wymagania

- Python 3.8+
- Konto Discord Bot (token)
- ID kanału Discord, na który mają być wysyłane wiadomości

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone <URL_REPOZYTORIUM>
cd "BOT DO RSS FEEDÓW"
```

2. Utwórz i aktywuj środowisko wirtualne:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

3. Zainstaluj zależności:
```bash
pip install python-dotenv feedparser discord.py aiohttp
```

## Konfiguracja

### 1. Token Discord

Utwórz plik `.env` w głównym katalogu projektu:
```bash
DISCORD_BOT_TOKEN=twoj_token_tutaj
```

**Jak uzyskać token:**
1. Przejdź do [Discord Developer Portal](https://discord.com/developers/applications)
2. Utwórz nową aplikację lub wybierz istniejącą
3. Przejdź do zakładki "Bot"
4. Skopiuj token (jeśli nie widzisz, kliknij "Reset Token")

### 2. Feedy RSS

Edytuj plik `feeds.json`:
```json
{
    "https://example.com/rss": 1234567890,
    "https://another-feed.com/rss": 9876543210
}
```

**Format:**
- Klucz: URL do feedu RSS
- Wartość: ID kanału Discord (liczba)

**Jak uzyskać ID kanału:**
1. Włącz tryb dewelopera w Discord (Ustawienia → Zaawansowane → Tryb dewelopera)
2. Kliknij prawym przyciskiem na kanał → "Kopiuj identyfikator"

## Uruchomienie

### Linux/Mac:
```bash
./start_bot.sh
```

### Ręcznie:
```bash
./venv/bin/python bot.py
```

### Windows:
```bash
venv\Scripts\python bot.py
```

## Funkcje

- ✅ Automatyczne sprawdzanie feedów RSS co 60 sekund
- ✅ Publikowanie nowych wpisów na Discord
- ✅ Wykrywanie obrazków i wideo (YouTube, Vimeo)
- ✅ Formatowanie wiadomości jako embedy Discord
- ✅ Pamiętanie opublikowanych postów (brak duplikatów)
- ✅ Obsługa wielu feedów jednocześnie
- ✅ Automatyczne czyszczenie starej historii

## Struktura plików

```
.
├── bot.py              # Główny plik bota
├── .env                # Token Discord (NIE COMMITUJ!)
├── feeds.json          # Lista feedów RSS
├── posted.json         # Historia opublikowanych postów (auto-generowany)
├── bot.log             # Logi działania bota (auto-generowany)
├── start_bot.sh        # Skrypt startowy
└── venv/               # Środowisko wirtualne
```

## Konfiguracja zaawansowana

W pliku `bot.py` możesz dostosować:

```python
CHECK_INTERVAL = 60          # Interwał sprawdzania (sekundy)
MAX_DESCRIPTION_LENGTH = 4096 # Maksymalna długość opisu
MAX_POSTED_LINKS = 1000      # Ile linków zapamiętywać
MAX_POSTS_PER_CYCLE = 0      # Limit postów na cykl (0 = bez limitu)
```

## Rozwiązywanie problemów

### Bot nie startuje
- Sprawdź czy token w `.env` jest poprawny
- Upewnij się, że zainstalowałeś wszystkie zależności

### Brak wiadomości na kanale
- Sprawdź czy bot ma uprawnienia do pisania na kanale
- Zweryfikuj ID kanału w `feeds.json`
- Sprawdź logi w `bot.log`

### Bot nie wykrywa nowych postów
- Sprawdź czy feed RSS działa (otwórz w przeglądarce)
- Usuń `posted.json` aby wymusić ponowne sprawdzenie

## Licencja

MIT License - możesz swobodnie używać i modyfikować.

## Autor

Stworzony z pomocą AI dla społeczności Discord.
