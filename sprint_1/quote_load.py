import logging

import requests

from custom_errors import (
    NoResponseFromQuoteUrl,
    JSONExtractError
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Quote_Load_Logger")


def get_response(quote_url):
    try:
        logger.info("Looking for the inspiring quote...")
        quote_response = requests.get(quote_url)
    except requests.exceptions.RequestException as e:
        logger.info("No response from Quote url")
        logger.info(e)
        raise NoResponseFromQuoteUrl("No response from Quote url")

    return quote_response


def get_quote(quote_url):
    quote_response = get_response(quote_url)
    try:
        response_dict = quote_response.json()
    except requests.exceptions.JSONDecodeError as e:
        logger.info("Response could not be serialized")
        logger.info(e)
        raise JSONExtractError("Response could not be serialized")

    try:
        quote_text = response_dict[0]["q"]
        logger.info("Quote text extracted successfully")
        quote_author = response_dict[0]["a"]
        logger.info("Quote author extracted successfully")
    except KeyError as e:
        logger.info("No such key in Response dict")
        logger.info(e)
        raise KeyError("No such key in Response dict")
    logger.info(f"\nQuote:{quote_text}\n"
                f"Author:{quote_author}")
    return quote_text, quote_author


if __name__ == "__main__":
    get_quote("https://zenquotes.io/api/random")


"""    
if mode == "text":
        json_key = "q"
        logger.info("Quote text string extracting...")
    elif mode == "author":
        json_key = "a"
        logger.info("Quote author string extracting...")
    else:
        logger.info(f"No such mode: {mode} in this function")
        raise NoSuchModeImplemented(f"No such mode: {mode} in this function")
        
"""
