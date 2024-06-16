from scripts.image_load import random_images
from scripts.message_send_requests import send_message_requests
from scripts.quote_and_image_compiler import put_quote_on_image
from scripts.quote_load import get_quote


def main_quote_on_image(pexel_api_key, webhook_teams, quote_url, message_sender_name):
    quote_text, quote_author = get_quote(quote_url)  # Getting quote and it's author from zenquotes
    image_url = random_images(pexel_api_key)  # Getting new image url from Pexel API
    encoded_image = put_quote_on_image(image_url, quote_text, quote_author)
    send_message_requests(webhook_teams,encoded_image, message_sender_name)  # Sending message to Teams channel

