from logging import DEBUG, getLogger, StreamHandler
import logging
import os
import sys
import time

import requests
from datetime import timedelta
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import InvalidDataError, InvalidResponseError


load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

log_format = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
SLEEP_AFTER_ERROR_TIME = 300
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Check the vailability of main tokens."""
    tokens = (
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    )
    missing_tokens = []
    for name, value in tokens:
        if value is None:
            missing_tokens.append(name)
    if missing_tokens:
        logger.critical('Missed the obligatory element in env')
        raise KeyError('Unvailable nessesary element of env')


def send_message(bot, message):
    """Send message with status in Telegram."""
    logger.debug('Try to send message to Telegram')
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        logger.error(f'Message was not sent: {error}')
        return False
    logger.debug(f'Message was sent: {message}')
    return True


def get_api_answer(timestamp):
    """Make a request to Yandex Practicum API."""
    payload = {'from_date': timestamp}
    response = requests.get(
        ENDPOINT, headers=HEADERS, params=payload)     
    if response.status_code == 400:
        code = response['code']
        error = response['error']
        raise InvalidResponseError(
            code=code,
            message=f'400 Bad request : {error}')
    if response.status_code == 401:
        error_code = response.get('code')
        message = response.get('message')
        raise InvalidResponseError(
            code=error_code,
            message=f'Ошибка с кодом {error_code} : {message}')
    if response.status_code != 200:
        raise ValueError(f"Unexpected status code: {response.status_code}") 

    homework_data = response.json()
    return homework_data


def check_response(homework_data):
    """Check the response from the Yandex Practicum."""
    homeworks = homework_data.get('homeworks')
    if homeworks == []:
        logger.debug('The list of homeworks is empty')
        raise InvalidDataError(message='The list of homeworks is empty')
    if type(homeworks) is not list:
        raise TypeError('It is not the list of homeworks')
    if type(homeworks[0]) is not dict:
        raise TypeError('There is no dictionary inside of homeworks')


def parse_status(homework):
    """Parse the status and name of homework from the response."""
    homework_status = homework['status']
    if homework_status is None:
        raise InvalidDataError(message='There is no status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise InvalidDataError(message='There is no an appropriate status')
    homework_name = homework['homework_name']
    if homework_name is None:
        raise InvalidDataError(message='There is no homework_name')

    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    # Создаем объект класса бота
    check_tokens()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    day_number = 60
    timestamp = int(time.time() - timedelta(days=day_number).total_seconds())
    previews_work = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            last_work = response.get('homeworks')[0]
            if last_work != previews_work:
                status_message = parse_status(last_work)
                previews_work = last_work
                bot.send_message(TELEGRAM_CHAT_ID, status_message)
            logger.debug('There is no a new status')
        except InvalidDataError as e:
            logger.debug(
                f'Error of response. Code {e.code}. Message: {e.message}')
            main()
        except InvalidResponseError as e:
            logger.error(
                f'Error of response. Code {e.code}. Message: {e.message}')
            time.sleep(SLEEP_AFTER_ERROR_TIME)
            main()
        except Exception as error:
            message = f'Unfamiliar error: {error}'
            logger.error(message)
            raise SystemExit(1)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
