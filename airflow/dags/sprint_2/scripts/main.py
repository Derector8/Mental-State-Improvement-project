from scripts.image_load import (
    random_images,
    search_images
)
from scripts.message_sent import (
    prepare_content_string,
    send_message,
    prepare_content_string_toads
)
from scripts.quote_load import get_quote


def main(pexel_api_key, webhook_teams, quote_url, message_sender_name):
    image_url = random_images(pexel_api_key)   # Getting new image url from Pexel API
    quote_text, quote_author = get_quote(quote_url)   # Getting quote and it's author from zenquotes
    content_string = prepare_content_string(quote_text, quote_author, image_url)   # Preparing formatted content string
    send_message(webhook_teams, content_string, message_sender_name)   # Sending message to Teams channel

def main_msi_4(pexel_api_key, webhook_teams, message_sender_name):
    image_url = search_images(pexel_api_key)  # Getting new image url from Pexel API
    content_string = prepare_content_string_toads(image_url)  # Preparing formatted content string
    send_message(webhook_teams, content_string, message_sender_name)  # Sending message to Teams channel


