# Telegram-бот «Практикум Домашка»
Бот автоматически проверяет статус домашних работ на Яндекс.Практикуме и присылает уведомления в Telegram, когда появляется новый результат проверки.

## Возможности

- Периодически обращается к API Яндекс.Практикума.
- Определяет изменения в статусе домашних заданий.
- Отправляет сообщение в указанный чат Telegram.
- Логирует все этапы работы для удобной отладки.

## Технологии

- Python 3.9+
- python-telegram-bot / pyTelegramBotAPI (telebot)
- requests
- python-dotenv

## Установка и запуск

1. Клонируйте репозиторий:
```
git clone https://github.com/AlinaGay/homework-bot.git
cd homework-bot
```

2. Создайте и активируйте виртуальное окружение (рекомендуется):
```
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. Создайте файл .env в корне проекта и укажите токены:
```
PRACTICUM_TOKEN=<токен_Яндекс.Практикум_API>
TELEGRAM_TOKEN=<токен_вашего_Telegram-бота>
TELEGRAM_CHAT_ID=<ID_чата_куда_присылать_уведомления>
```

5. Запустите бота:
```
python homework.py
```

Бот будет опрашивать API каждые 10 минут (значение RETRY_PERIOD) и присылать обновления в Telegram.

| [Alina Opolskaia](https://github.com/AlinaGay/) |
| Backend Developer • Python Engineer  
