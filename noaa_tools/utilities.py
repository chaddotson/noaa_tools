from io import BytesIO
from PIL import Image
from requests import get

__author__ = 'Chad Dotson'


def get_image_from_url(url):
    response = get(url, headers={
        'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
    })

    return Image.open(BytesIO(response.content))