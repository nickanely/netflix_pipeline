import logging
from datetime import time, datetime
import requests

main_formatter = logging.Formatter('%(asctime)s => %(name)s => %(levelname)s => %(message)s => %(filename)s')

# 1. Create your own logging infrastructure
logger = logging.getLogger('task_1_2_3')
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add formatter to handlers
file_handler.setFormatter(main_formatter)
console_handler.setFormatter(main_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# 3. Implementing custom filter: 1 points
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


# 2. Implement custom Handler
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


slack_handler = SlackHandler('https://hooks.slack.com/services/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')
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(main_formatter)

logger.addHandler(slack_handler)
logger.addFilter(Filter(time(0, 1), time(23, 59)))

logger.info('test_1')
