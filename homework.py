import os
import requests
import time

from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

practicum_token = os.getenv('PRACTICUM_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {practicum_token}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     """."""
#     bot.send_message(chat_id=, f"Ваш ID: {message.chat.id}")
#     print(f"Ваш chat_id: {message.chat.id}")


def check_tokens():
    """Check the vailability of main tokens."""
    if not (practicum_token or telegram_token or chat_id):
        raise Exception('Sorry! You dont have tokens for the lunch of homework_of_alina_bot.')


def send_message(bot, message):
    """Send message with status in Telegram."""
    bot.send_message(chat_id=chat_id, text=message)


def get_api_answer(timestamp):
    """Make a request to Yandex Practicum API."""
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception as error:
        print(error)
        new_endpoint = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
        homework_statuses = requests.get(
            new_endpoint, headers=HEADERS, params=payload)
    response = homework_statuses.json()
    return response


def check_response(response):
    """Check the response from the Yandex Practicum."""
    if (response.get('homeworks') is None
            and response.get('current_date') is None):
        raise Exception('Sorry! Your response is not correct.')


def parse_status(homework):
    """Parse the status and name of homework from the response."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    # Создаем объект класса бота
    bot = TeleBot(token=telegram_token)
    timestamp = int(time.time())
    # check_tokens()
    # bot.send_message(chat_id, 'Hi!')
    status = ''
    print(status)
    bot.polling(non_stop=True)

    while True:
        try:
            check_tokens()
            response = get_api_answer(0)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            print(message)
        else:
            print(response.get('homeworks'))
            last_work = response.get('homeworks')[0]
            if last_work['status'] != status:
                status_message = parse_status(last_work)
                status = last_work['status']
                bot.send_message(chat_id, status_message)


if __name__ == '__main__':
    main()
