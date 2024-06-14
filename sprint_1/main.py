from image_load import curated_photos
from quote_load import get_quote
from message_sent import prepare_content_string, send_message
from credentials import PEXEL_API_KEY, WEBHOOK_TEAMS, QUOTE_URL, OWNER


def main(pexel_api_key, webhook_teams, quote_url, owner):
    image_url = curated_photos(pexel_api_key)   # Getting new image url from Pexel API
    quote_text, quote_author = get_quote(quote_url)   # Getting quote and it's author from zenquotes
    content_string = prepare_content_string(quote_text, quote_author, image_url)   # Preparing formatted content string
    send_message(webhook_teams, content_string, owner)   # Sending message to Teams channel


if __name__ == "__main__":
    main(PEXEL_API_KEY, WEBHOOK_TEAMS, QUOTE_URL, OWNER)
