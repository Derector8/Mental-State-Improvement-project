import pymsteams
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Teams_Send_Message_Logger")


class MessageException(Exception):
    pass


class WebhookUrlError(MessageException):
    pass


def prepare_content_string(quote_text, quote_author, image_url):
    logger.info('Preparing content string...')
    content_string = f"{quote_text}\n\n" \
                     f"Author: {quote_author}\n\n" \
                     f"![Image]({image_url})"
    logger.info('Content string created')
    return content_string


def send_message(webhook_teams, content_string, owner):
    try:
        logger.info('Preparing Teams Connection...')
        card = pymsteams.connectorcard(webhook_teams)
        logger.info('Preparing message...')
        card.title(f"{owner}'s Daily Inspiring Quote=)")
        card.text(content_string)
        logger.info('Sending message to Teams...')
        card.send()
        logger.info('Message successfully sent!')
    except requests.exceptions.MissingSchema as e:
        logger.info('Invalid Webhook Url')
        logger.info(e)

        raise WebhookUrlError('Invalid Webhook Url')


def process(webhook_teams, quote_text, quote_author, image_url, owner):
    send_message(webhook_teams, prepare_content_string(quote_text, quote_author, image_url), owner)


if __name__ == '__main__':
    pass
