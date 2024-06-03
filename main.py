from image_load import get_image_url
from quote_load import get_quote
from message_sent import process
from credentials import PEXEL_API_KEY, WEBHOOK_TEAMS, QUOTE_URL, OWNER


def main(pexel_api_key, webhook_teams, quote_url, owner):
    image_url = get_image_url(pexel_api_key)   # Getting new image url from Pexel API
    quote_text, quote_author = get_quote(quote_url)   # Getting quote and it's author from zenquotes
    process(webhook_teams, quote_text, quote_author, image_url, owner)   # Sending quote/image in Teams


if __name__ == '__main__':
    main(PEXEL_API_KEY, WEBHOOK_TEAMS, QUOTE_URL, OWNER)
