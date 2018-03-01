#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""deal with downloading modifying and uploading images"""
from typing import List

import requests
import os
import subprocess
from io import BytesIO

from PIL import Image as Im
from PIL.Image import Image


SUPPORTED_IMAGE_TYPES = {"PNG", "JPEG", "JPG", "GIF"}

MAX_SIZE = 50000000


def make_primitive_image_io(image: Image, image_type: str,
                            shape_number: int) -> BytesIO:
    """Use sylvaindumont/primitive/:pr to make a primitive image"""
    byteimgio = BytesIO()

    # save image into memory
    image.save(byteimgio, image_type)

    # move to front of file
    byteimgio.seek(0)

    # run the primitive command
    process = subprocess.run(
        "primitive -i - -o - -n {}".format(shape_number),
        input=byteimgio.read(),
        stdout=subprocess.PIPE,
        shell=True
    )

    return BytesIO(process.stdout)


def primify_attachment(attachment: dict, shape_number: int) -> BytesIO:
    """Convert a discord image attachment to a primitive image"""
    filename, file_extension = os.path.splitext(attachment.get("filename"))
    file_extension = file_extension.lstrip(".").upper()
    file_size = attachment.get("size")

    if file_extension not in SUPPORTED_IMAGE_TYPES:
        raise TypeError("Image type: {} is not supported".format(file_extension))

    if file_size > MAX_SIZE:
        raise ValueError("Image is to large: {}".format(file_size))

    url = attachment["url"]
    return make_primitive_image_io(
        image=Im.open(requests.get(url, stream=True).raw),
        image_type=file_extension,
        shape_number=shape_number,
    )


