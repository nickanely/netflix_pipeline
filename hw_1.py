import logging.config
from datetime import datetime, time
import pandas as pd
import requests

main_formatter = logging.Formatter('%(asctime)s => %(name)s => %(levelname)s => %(message)s => %(filename)s')


class SlackHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            "text": log_entry
        }
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending log entry to Slack: {e}")


# 4. Create a logging config file and figure out how to apply it: 1 point
logging.config.fileConfig('config.ini')
logger = logging.getLogger('homework')

# Apply this configuration to any of your pet projects (3 points)
df = pd.DataFrame()
try:
    df = pd.read_csv('netfix_TV_Shows_and_Movies.csv')
except FileNotFoundError as e:
    logger.error(f'file was not found {e}')
    logger.critical('This is critical situation')

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
