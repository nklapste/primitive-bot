#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""deal with downloading modifying and uploading images"""


import requests
import os
import subprocess
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image


SUPPORTED_IMAGE_TYPES = {".png"}
MAX_SIZE = 50000000


def download_image_attachments(attachments: list):
    """Download and open an image"""
    images = []
    for attachment in attachments:
        filename, file_extension = os.path.splitext(attachment.get("filename"))
        file_size = attachment.get("size")
        if file_extension in SUPPORTED_IMAGE_TYPES and file_size < MAX_SIZE:
            url = attachment.get("url")
            images.append(Image.open(requests.get(url, stream=True).raw))
    return images


def primify_image(image: Image.Image, shape_number: int):
    """Convert a image into primtive image"""
    with TemporaryDirectory() as tempdir:
        input_path = os.path.join(tempdir, "temp_img_in.png")
        output_path = os.path.join(tempdir, "temp_img_out.png")
        image.save(input_path)
        image.close()
        return make_primitive_image(
            input_path,
            output_path,
            shape_number=shape_number
        )


def make_primitive_image(input_image_path: str, output_image_path: str,
                         shape_number: int, **kwargs) -> BytesIO:
    """Use fogleman/primitive to make a primitive image

    Pass the image data as a BytesIO object for later output

    :param input_image_path:
    :type input_image_path: str

    :param output_image_path:
    :type output_image_path: str

    :param shape_number:
    :type shape_number: int

    :param kwargs:
    :type kwargs: dict
    """
    primitive_command = ["%primitive%", "-i", input_image_path, "-o",
                         output_image_path, "-n", str(shape_number)]

    # run the primitive command
    subprocess.run(
        primitive_command,
        stdout=subprocess.PIPE,
        shell=True
    )

    # this io play allows us to open the image and dereference from the
    # disk
    # open image from disk
    out_image = Image.open(output_image_path)
    byteimgio = BytesIO()
    # save image into memory
    out_image.save(byteimgio, "PNG")
    byteimgio.seek(0)
    # open memory reffed image into memory
    return BytesIO(byteimgio.read())


def primify_images(images: list, shape_number: int):
    """take a list of images and convert them to primitive images"""
    primitive_images = []
    for image in images:
        primitive_images.append(primify_image(image, shape_number))
    return primitive_images


# TODO move to tests
MOCK_ATT = [
    {
        'width': 1920,
        'url': 'https://cdn.discordapp.com/attachments/340941251216015369/417828520375484437/screen_1920x1080_2018-01-23_20-02-35.903.png',
        'size': 1889296,
        'proxy_url': 'https://media.discordapp.net/attachments/340941251216015369/417828520375484437/screen_1920x1080_2018-01-23_20-02-35.903.png',
        'id': '417828520375484437',
        'height': 1080,
        'filename': 'screen_1920x1080_2018-01-23_20-02-35.903.png'
    }
]
