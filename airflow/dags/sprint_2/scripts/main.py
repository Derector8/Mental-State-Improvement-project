#from sprint_2.credentials import PEXEL_API_KEY, WEBHOOK_TEAMS, QUOTE_URL, OWNER
from sprint_2.scripts.image_load import (
    curated_photos,
    search_photos
)
from sprint_2.scripts.message_sent import (
    prepare_content_string,
    send_message,
    prepare_content_string_toads
)
from sprint_2.scripts.quote_load import get_quote


def main(pexel_api_key, webhook_teams, quote_url, owner):
    image_url = curated_photos(pexel_api_key)   # Getting new image url from Pexel API
    quote_text, quote_author = get_quote(quote_url)   # Getting quote and it's author from zenquotes
    content_string = prepare_content_string(quote_text, quote_author, image_url)   # Preparing formatted content string
    send_message(webhook_teams, content_string, owner)   # Sending message to Teams channel

def main_msi_4(pexel_api_key, webhook_teams, owner):
    image_url = search_photos(pexel_api_key)  # Getting new image url from Pexel API
    content_string = prepare_content_string_toads(image_url)  # Preparing formatted content string
    send_message(webhook_teams, content_string, owner)  # Sending message to Teams channel


