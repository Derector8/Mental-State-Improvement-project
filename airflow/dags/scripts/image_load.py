import logging
import random

import requests
from scripts.custom_errors import (
    APINotAvailable,
    PexelAPIKeyError,
    JsonError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Image_Load_Logger")


def search_images(pexel_api_key, key_word="toad", orientation="", size="", color="", page=1, per_page=80):
    term = "search"
    query_dict = {"query": key_word, "orientation": orientation, "size": size,
             "color": color, "page": page, "per_page": per_page}
    image_url = get_image_url(pexel_api_key, term, query_dict)
    return image_url


def random_images(pexel_api_key, page=1, per_page=80):
    term = "curated"
    query_dict = {"page": page, "per_page": per_page}
    image_url = get_image_url(pexel_api_key, term, query_dict)
    return image_url


def get_image_url(pexel_api_key, term, query, size="medium"):
    api_url = "https://api.pexels.com/v1/"
    headers = {"Authorization": pexel_api_key}
    logger.info("Connecting to Pexels API...")
    try:
        response = requests.get(f"{api_url}{term}",
                                headers=headers, params=query)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            raise PexelAPIKeyError("Check your Pexel_api_key")
        else:
            raise APINotAvailable("Check the availability of Pexel API "
                                  "or your internet connection ")
    logger.info("Getting image url from response...")
    try:
        image_pack = response.json()
        image_url = image_pack["photos"][random.randint(0, 79)]["src"][size]
        logger.info("Image url received")
    except requests.exceptions.JSONDecodeError:
        raise JsonError("Can't decode received JSON response")

    return image_url


def save_image_locally(image_url):
    # ToDo try/except
    if image_url:
        image_resp = requests.get(image_url)
        with open("../images/today_pic.jpg", "wb") as f:
            f.write(image_resp.content)
        logger.info("Image loaded successfully!")
    else:
        logger.error("Image loading failed!")


if __name__ == "__main__":
    save_image_locally("https://www.funnyart.club/uploads/posts/2023-04/1682881890_funnyart-club-p-krasivii-les-krasivo-1.jpg")

