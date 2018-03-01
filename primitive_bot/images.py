#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Deal with downloading and modifying (primifying) images"""

from typing import Tuple

from urllib.request import urlopen, Request
import os
import subprocess
from io import BytesIO

from PIL import Image as Im
from PIL.Image import Image

# TODO look into svglib 0.8.1 as a replacement
from cairosvg import svg2png

SUPPORTED_IMAGE_TYPES = {"PNG", "JPEG", "JPG", "GIF"}

MAX_SIZE = 50000000
MAX_SHAPES = 200


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


def primify_attachment(attachment: dict, shape_number: int) -> \
        Tuple[BytesIO, BytesIO]:
    """Convert a discord image attachment to a primitive image

    :return: Tuple of two BytesIO file-like objects of the primitive image
        one as a .svg the other as a .png
    """
    filename, file_extension = os.path.splitext(attachment.get("filename"))
    file_extension = file_extension.lstrip(".").upper()
    file_size = attachment.get("size")

    if file_extension not in SUPPORTED_IMAGE_TYPES:
        raise TypeError("image type: .{} is not "
                        "supported".format(file_extension))
    if file_size > MAX_SIZE:
        raise ValueError("image is too large: {}".format(file_size))
    if shape_number > MAX_SHAPES:
        raise ValueError("shape number must be equal to or less than 200")

    url = attachment["url"]

    # discord hates urllibs default headers, giving another UAS works fine
    req = Request(url, headers={'User-Agent': 'primitive-bot'})

    # make the primitive image
    primitive_image = make_primitive_image_io(
        image=Im.open(urlopen(req)),
        image_type=file_extension,
        shape_number=shape_number,
    )

    # make a png of the primitive image for displaying on discord
    display_image = BytesIO(svg2png(primitive_image.read()))

    # seek back to the start of the primitive image
    primitive_image.seek(0)

    return primitive_image, display_image
