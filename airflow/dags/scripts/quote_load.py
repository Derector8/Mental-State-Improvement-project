import logging

import requests

from scripts.custom_errors import (
    NoResponseFromQuoteUrl,
    JSONExtractError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Quote_Load_Logger")


def get_response(quote_url):
    try:
        logger.info("Looking for the inspiring quote...")
        quote_response = requests.get(quote_url)
    except requests.exceptions.RequestException:
        raise NoResponseFromQuoteUrl("No response from Quote url")

    return quote_response


def get_quote(**kwargs):
    quote_url = "https://zenquotes.io/api/random"
    quote_response = get_response(quote_url)
    try:
        response_dict = quote_response.json()
    except requests.exceptions.JSONDecodeError:
        raise JSONExtractError("Response could not be serialized")

    try:
        quote_text = response_dict[0]["q"]
        logger.info("Quote text extracted successfully")
    except KeyError:
        raise KeyError("No key 'q' in response dict")

    try:
        quote_author = response_dict[0]["a"]
        logger.info("Quote author extracted successfully")
    except KeyError:
        raise KeyError("No key 'a' in response dict")

    kwargs["ti"].xcom_push(key="quote_text", value=quote_text)
    kwargs["ti"].xcom_push(key="quote_author", value=quote_author)


def get_quote_toads(**kwargs):
    kwargs["ti"].xcom_push(key="quote_text", value="It's Wednesday, my Dudes!")
    kwargs["ti"].xcom_push(key="quote_author", value="")

if __name__ == "__main__":
    get_quote("https://zenquotes.io/api/random")
