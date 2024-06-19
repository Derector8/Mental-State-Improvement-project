import logging

import pymsteams
import requests

from custom_errors import WebhookUrlError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Teams_Send_Message_Logger")


def prepare_content_string(quote_text, quote_author, image_url):
    logger.info("Preparing content string...")
    content_string = (
                      f"{quote_text}\n\n"
                      f"**Author**: {quote_author}\n\n"
                      f"![Image]({image_url})"
    )
    logger.info("Content string created")
    return content_string


def send_message(webhook_teams, content_string, message_sender_name):
    try:
        logger.info("Preparing Teams Connection...")
        card = pymsteams.connectorcard(webhook_teams)
        logger.info("Preparing message...")
        card.title(f"{message_sender_name}'s Daily Inspiring Quote=)")
        card.text(content_string)
        logger.info("Sending message to Teams...")
        card.send()
        logger.info("Message successfully sent!")
    except requests.exceptions.MissingSchema as e:
        logger.info("Invalid Webhook Url")
        logger.info(e)
        raise WebhookUrlError("Invalid Webhook Url")


if __name__ == "__main__":
    content_string = prepare_content_string("quote_text", "quote_author", "image_url")
    send_message("webhook_teams", content_string, "owner")
