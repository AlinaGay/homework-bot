import logging
import os
import sys
import telebot
import time
from datetime import datetime, timedelta
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import StatusCodeNot200


load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

log_format = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
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
    """Checks for the availability of basic tokens."""
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
        logger.critical(
            f'The obligatory token is missed in environment: {missing_tokens}')
        raise ValueError(
            f'The obligatory token is missed in environment: {missing_tokens}')


def send_message(bot, message):
    """Sends message with status in Telegram."""
    logger.info('Try to send message to Telegram')
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    logger.debug(f'The message was sent: {message}')


def get_api_answer(timestamp):
    """Makes a request to Yandex Practicum API."""
    payload = {'from_date': timestamp}
    from_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
    logger.info(f'Makes a request to {ENDPOINT} from_date: {from_date}')
    try:
        response = requests.get(
            ENDPOINT, headers=HEADERS, params=payload)
    except requests.RequestException as error:
        raise ConnectionError(f'Here is error: {error} '
                              f'during the attempto to request to {ENDPOINT} '
                              f'with from_date: {from_date}')
    if response.status_code != HTTPStatus.OK:
        raise StatusCodeNot200(
            f"Code of answer from API: {response.status_code}",
            code=response.status_code)

    logger.info(
        f'Successfully made a request to {ENDPOINT} '
        f'with from_date: {from_date}')
    return response.json()


def check_response(response):
    """Checks the response from the Yandex Practicum API."""
    logger.info('Check the response from API')
    if not isinstance(response, dict):
        raise TypeError(f'Error type of data in response: {type(response)}')

    homeworks = response.get('homeworks')
    if homeworks is None:
        raise KeyError('There is no key \'homeworks\'')
    if not isinstance(homeworks, list):
        raise TypeError(f'There is no a list of homeworks: {type(homeworks)}')

    logger.info('The end of cheking response from API')


def parse_status(homework):
    """Parses the status and name of homework from the response."""
    logger.info('Parses the status and name of homework from the response.')
    homework_keys = ('homework_name', 'status')
    missing_keys = []

    for key in homework_keys:
        if key not in homework:
            missing_keys.append(key)
    if missing_keys:
        raise KeyError(f'There is no key: {missing_keys}')

    homework_name = homework['homework_name']
    homework_status = homework['status']

    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(
            f'There is no an appropriate status: {homework_status}')

    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """The basic logic of the bot's operation."""
    check_tokens()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previews_homeworks = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            homeworks_list = response.get('homeworks')
            if homeworks_list == []:
                logger.debug('The list of homeworks is empty')
                continue
            homeworks = response.get('homeworks')[0]
            if homeworks != previews_homeworks:
                status_message = parse_status(homeworks)
                previews_homeworks = homeworks
                send_message(bot, status_message)
            if response.get('current_date'):
                timestamp = response.get('current_date')
            else:
                logger.debug('There is no a new status')
        except (telebot.apihelper.ApiException
                or requests.exceptions.RequestException) as error:
            logger.exception(f'Message was not sent: {error}')
        except Exception as error:
            message = f'Unfamiliar error: {error}'
            logger.error(message)
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
