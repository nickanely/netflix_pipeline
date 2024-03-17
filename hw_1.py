import logging
import logging.config
from datetime import datetime, time

import pandas as pd
import telebot

chat_id = '6249231839'
token = '6997477472:AAGaJznKxVvNpi_g5HuvqILbEf3fFQTFgBc'
main_formatter = logging.Formatter('%(asctime)s => %(name)s => %(levelname)s => %(message)s => %(filename)s')


# filter to receive logs during specific time. maybe no real life use, but practice
class Filter(logging.Filter):
    def __init__(self, start_time, end_time):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

    def filter(self, record):
        current_time = datetime.now().time()
        if self.start_time <= current_time <= self.end_time:
            return True
        else:
            return False


class TelegramBot(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord):
        bot = telebot.TeleBot(self.token)
        bot.send_message(self.chat_id, self.format(record))


critical_logger = logging.getLogger()

tg_bot_handler = TelegramBot(token, chat_id)
tg_bot_handler.setLevel(logging.CRITICAL)
tg_bot_handler.setFormatter(main_formatter)

critical_logger.addHandler(tg_bot_handler)


logging.config.fileConfig('config.ini')
logger = logging.getLogger(__name__)
logger.addFilter(Filter(time(0, 1), time(23, 59)))

df = pd.DataFrame()

try:
    df = pd.read_csv('netflix_TV_Shows_and_Movies.csv')
except FileNotFoundError as e:
    logger.error(f'file was not found {e}')
    critical_logger.critical('This is critical situation')

movies_count = 0
shows_count = 0
total_count = 0
try:
    logger.info('checking attribute names ...')
    type_counts = df['type'].value_counts()
    movies_count = type_counts.get('MOVIE', 0)
    shows_count = type_counts.get('SHOW', 0)
    total_count = movies_count + shows_count
except KeyError as k:
    logger.error(f'attribute`s name is wrong {k}')
except TypeError as e:
    logger.error(f'attribute is wrong {e}')

logger.info('checking total count and calculating ratio ...')
if total_count == 0:
    movies_ratio = 0
    shows_ratio = 0
else:
    movies_ratio = movies_count / total_count
    shows_ratio = shows_count / total_count

print(f"Ratio of Movies: {movies_ratio:.2f}")
print(f"Ratio of TV Shows: {shows_ratio:.2f}")
