import logging
import random

import requests

from sprint_2.scripts.custom_errors import (
    APINotAvailable,
    PexelAPIKeyError,
    JsonError
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Image_Load_Logger")


def search_photos(pexel_api_key, query="toad", orientation="", size="", color="", page=1, per_page=80):
    term = "search"
    query = {"query": query, "orientation": orientation, "size": size,
             "color": color, "page": page, "per_page": per_page}
    photos = get_image_url(pexel_api_key, term, query, )
    return photos


def curated_photos(pexel_api_key, page=1, per_page=80):
    term = "curated"
    query = {"page": page, "per_page": per_page}
    image_url = get_image_url(pexel_api_key, term, query)
    return image_url


def get_image_url(pexel_api_key, term, query):
    api_url = "https://api.pexels.com/v1/"
    headers = {"Authorization": pexel_api_key}
    logger.info("Connecting to Pexels API...")
    try:
        response = requests.get(f"{api_url}{term}",
                                headers=headers, params=query)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            logger.info("Problems with your Pexel_api_key")
            logger.info(e)
            raise PexelAPIKeyError("Check your Pexel_api_key")
        else:
            logger.info("Pexel's API Unavailable. Can't receive image")
            logger.info(e)
            raise APINotAvailable("Check the availability of Pexel API "
                                  "or your internet connection ")
    logger.info("Getting image url from response...")
    try:
        image_pack = response.json()
        image_url = image_pack["photos"][random.randint(0, 79)]["src"]["tiny"]
        logger.info("Image url received")
    except requests.exceptions.JSONDecodeError as e:
        logger.info("Something wrong with received json")
        logger.info(e)
        raise JsonError("Can't decode received JSON response")

    return image_url


def save_image_locally(image_url):
    # ToDo try/except
    if image_url:
        image_resp = requests.get(image_url)
        with open("today_pic.jpg", "wb") as f:
            f.write(image_resp.content)
        logger.info("Image loaded successfully!")
    else:
        logger.info("Image loading failed!")


if __name__ == "__main__":
    curated_photos("api_key")
    save_image_locally(curated_photos("api_key"))
