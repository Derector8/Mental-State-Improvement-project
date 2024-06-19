import base64
import logging
import textwrap as tw
from io import BytesIO

import requests
from PIL import Image, ImageDraw

from scripts.custom_errors import NoResponseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Quote_on_Image_Logger")


def _get_image(image_url):
    logger.info("Getting image from url...")

    try:
        image_response = requests.get(image_url)
    except requests.exceptions.RequestException:
        raise NoResponseError(f"No response from url:{image_url}")

    logger.info("Image received")
    raw_image = image_response.content
    return raw_image


def _put_quote_on_image(**kwargs):
    image_url = kwargs["ti"].xcom_pull(key="image_url")
    quote_text = kwargs["ti"].xcom_pull(key="quote_text")
    quote_author = kwargs["ti"].xcom_pull(key="quote_author")
    raw_image = _get_image(image_url)

    logger.info("Image transformation started...")
    image = Image.open(BytesIO(raw_image)).resize((350, 350))
    draw = ImageDraw.Draw(image)

    wrapped_quote = tw.fill(quote_text, width=30)
    text = wrapped_quote + "\nAuthor: " + quote_author
    position = (30, 0)
    bbox = draw.textbbox(position, text, font_size=20)
    draw.rectangle(bbox, fill="white")
    draw.multiline_text(
        position,
        text,
        fill="black",
        spacing=2,
        font_size=20,
        align="center",
    )
    logger.info("Transformation ended. Saving image...")

    buf = BytesIO()
    image.save(buf, format="jpeg")

    return buf


def prepare_image(**kwargs):
    buffered_image = _put_quote_on_image(kwargs)

    logger.info("Encoding image...")
    image_data = base64.b64encode(buffered_image.getbuffer()).decode("utf-8")
    encoded_image = f"data:image/jpeg;base64,{image_data}"
    logger.info("Image encoded")

    kwargs["ti"].xcom_push(key="encoded_image", value=encoded_image)
