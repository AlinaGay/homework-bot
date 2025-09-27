# Telegram Bot “Practicum Homework”
The bot automatically checks the status of homework on Yandex.Practicum and sends notifications to Telegram when a new review result appears.

## Features
- Periodically queries the Yandex.Practicum API.
- Detects changes in homework review statuses.
- Sends a message to the specified Telegram chat.
- Logs all stages of operation for easier debugging.

## Technologies
- Python 3.9+
- python-telegram-bot / pyTelegramBotAPI (telebot)
- requests
- python-dotenv

## Installation and Run
Clone the repository:
```bash
git clone https://github.com/AlinaGay/homework-bot.git
cd homework-bot
```

2. Create and activate a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a .env file in the project root and specify the tokens:
```
PRACTICUM_TOKEN=<токен_Яндекс.Практикум_API>
TELEGRAM_TOKEN=<токен_вашего_Telegram-бота>
TELEGRAM_CHAT_ID=<ID_чата_куда_присылать_уведомления>
```

5. Run the bot:
```
python homework.py
```

The bot will poll the API every 10 minutes (RETRY_PERIOD) and send updates to Telegram.

| [Alina Opolskaia](https://github.com/AlinaGay/) |
| Backend Developer • Python Engineer  
