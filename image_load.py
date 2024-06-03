from pexelsapi.pexels import Pexels
import requests
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Image_Load_Logger")


class ImageException(Exception):
    pass


class APINotAvailable(ImageException):
    pass


class PexelAPIKeyError(ImageException):
    pass


def get_image_url(pexel_api_key):
    try:
        logger.info('Connecting to Pexels API...')
        pexel = Pexels(pexel_api_key)
        search_photos = pexel.curated_photos(page=1, per_page=80)
        logger.info('Getting image url...')
        image_url = search_photos['photos'][random.randint(0, 79)]['src']['tiny']
        logger.info('Image url received')

        return image_url

    except requests.exceptions.JSONDecodeError as e:
        logger.info("Pexel's API Unavailable. Can't receive image url")
        logger.info(e)

        raise APINotAvailable('Check the availability of Pexel API')

    except KeyError as e:
        logger.info("Check your Pexel_api_key")
        logger.info(e)

        raise PexelAPIKeyError('Check your Pexel_api_key')


def save_image_locally(image_url):
    # ToDo try/except
    if image_url:
        image_resp = requests.get(image_url)
        with open("today_pic.jpg", "wb") as f:
            f.write(image_resp.content)
        logger.info('Image loaded successfully!')
    else:
        logger.info('Image loading failed!')


if __name__ == "__main__":
    get_image_url('url')
    save_image_locally('image_url')
