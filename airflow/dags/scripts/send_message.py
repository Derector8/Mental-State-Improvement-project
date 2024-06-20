import requests
import logging

from scripts.custom_errors import WebhookUrlError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Teams_Send_Message_Requests_Logger")

def send_message(webhook_url, message_sender_name, **kwargs):
    image = kwargs["ti"].xcom_pull(key="encoded_image")

    json_data = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"{message_sender_name}'s Inspiring Quote=)",
                            "weight": "bolder",
                            "size": "medium",
                        },
                        {
                            "type": "Image",
                            "url": f"{image}",
                        },
                    ],
                },
            },
        ],
    }

    logger.info("Trying to send Teams message...")

    try:
        response = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            json=json_data
        )
        response.raise_for_status()

    except requests.exceptions.MissingSchema:
        logger.error("Message couldn't be sent. Check your webhook url")
        raise WebhookUrlError("Invalid Webhook Url")

    except requests.exceptions.HTTPError as e:
        logger.error("Message couldn't be sent")
        raise e

    logger.info("Message successfully sent!")
