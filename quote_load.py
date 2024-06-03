import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Quote_Load_Logger")


class QuoteException(Exception):
    pass


class NoResponseFromQuoteUrl(QuoteException):
    pass


def get_quote(quote_url):
    try:
        logger.info('Looking for the inspiring quote...')
        quote_resp = requests.get(quote_url)
        quote_text = quote_resp.json()[0]['q']
        logger.info('Quote text load success')
        quote_author = quote_resp.json()[0]['a']
        logger.info('Quote author load success')

        return quote_text, quote_author
    except requests.exceptions.RequestException as e:
        logger.info('No response from Quote url')
        logger.info(e)

        raise NoResponseFromQuoteUrl('No response from Quote url')

    except KeyError as e:
        logger.info('No such key in Response dict')
        logger.info(e)

        raise KeyError('No such key in Response dict')


if __name__ == "__main__":
    get_quote('quote_url')
