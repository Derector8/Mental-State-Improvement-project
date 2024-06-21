import logging
import random

from airflow.models import Variable

import requests
from scripts.custom_errors import (
    APINotAvailable,
    PexelAPIKeyError,
    JsonError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Image_Load_Logger")


def search_images(
        key_word="toad",
        orientation="",
        size="",
        color="",
        page=1,
        per_page=80,
        **kwargs,
):
    pexel_api_key = Variable.get("secret_pexel_api_key")
    term = "search"
    query_dict = {
        "query": key_word,
        "orientation": orientation,
        "size": size,
        "color": color,
        "page": page,
        "per_page": per_page,
    }
    image_url = get_image_url(pexel_api_key, term, query_dict)
    kwargs["ti"].xcom_push(key="image_url", value=image_url)


def random_images(
        page=1,
        per_page=80,
        **kwargs,
):
    pexel_api_key = Variable.get("secret_pexel_api_key")
    term = "curated"
    query_dict = {"page": page, "per_page": per_page}
    image_url = get_image_url(pexel_api_key, term, query_dict)
    kwargs["ti"].xcom_push(key="image_url", value=image_url)


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
