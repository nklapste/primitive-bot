#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Deal with downloading and primifying images"""

from typing import Tuple

from urllib.request import urlopen, Request
import os
import subprocess
from io import BytesIO

from PIL import Image as Im
from PIL.Image import Image

from cairosvg import svg2png

SUPPORTED_IMAGE_TYPES = {"PNG", "JPEG", "JPG", "GIF"}

MAX_SIZE = 50000000
MAX_SHAPES = 200
MAX_EXTRA_SHAPES = 20
SHAPE_DICT = {
    "combo": 0,
    "triangle": 1,
    "rectangle": 2,
    "ellipse": 3,
    "circle": 4,
    "rotatedrectangle": 5,
    "beziers": 6,
    "rotatedellipse": 7,
    "polygon": 8,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8
}


def validate_primify_args(shape_number: int, shape_type: str,
                          extra_shapes: int):
    """Validate primify attachment arguments"""
    if shape_number > MAX_SHAPES:
        raise ValueError("shape number must be equal to or less than 200")

    if shape_type not in SHAPE_DICT:
        raise ValueError(
            "Shape type: {} not in supported shapes: {}".format(
                shape_type,
                SHAPE_DICT.keys()
            )
        )

    if extra_shapes > MAX_EXTRA_SHAPES:
        raise ValueError("Extra shape number must be equal to or less than 20")


def make_primitive_image_io(image: Image, image_type: str, shape_number: int,
                            shape_type: str, extra_shapes: int) -> BytesIO:
    """Use sylvaindumont/primitive/:pr to make a primitive image"""
    # translate shape type string to shape number
    shape_type = SHAPE_DICT[shape_type]

    byteimgio = BytesIO()

    # save image into memory
    image.save(byteimgio, image_type)

    # move to front of file
    byteimgio.seek(0)

    # run the primitive command
    process = subprocess.run(
        "primitive -i - -o - -n {} -m {} -rep {}".format(
            shape_number,
            shape_type,
            extra_shapes
        ),
        input=byteimgio.read(),
        stdout=subprocess.PIPE,
        shell=True,
        check=True
    )

    return BytesIO(process.stdout)


def primify_attachment(attachment: dict, shape_number: int, shape_type: str,
                       extra_shapes: int) -> Tuple[BytesIO, BytesIO]:
    """Convert a discord image attachment to a primitive image

    :return: Tuple of two BytesIO file-like objects of the primitive image
        one as a .svg the other as a .png
    """
    filename, file_extension = os.path.splitext(attachment.get("filename"))
    file_extension = file_extension.lstrip(".").upper()
    file_size = attachment.get("size")

    if file_extension not in SUPPORTED_IMAGE_TYPES:
        raise TypeError("Image type: .{} is not "
                        "supported".format(file_extension))
    if file_size > MAX_SIZE:
        raise ValueError("Image is too large: {}".format(file_size))

    # discord hates urllibs default headers, giving another UAS works fine
    req = Request(attachment["url"], headers={'User-Agent': 'primitive-bot'})

    # make the primitive image
    primitive_image = make_primitive_image_io(
        image=Im.open(urlopen(req)),
        image_type=file_extension,
        shape_number=shape_number,
        shape_type=shape_type,
        extra_shapes=extra_shapes
    )

    # make a png of the primitive image for displaying on discord
    display_image = BytesIO(svg2png(primitive_image.read()))

    # seek back to the start of the primitive image
    primitive_image.seek(0)

    return primitive_image, display_image
