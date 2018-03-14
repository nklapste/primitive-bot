#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""primitive-bot Discord bot api"""

from uuid import uuid4
from logging import getLogger

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from primitive_bot.images import primify_attachment


DESCRIPTION = """primitive-bot a Discord bot that converts inputted images
into primitive vector based graphics."""


BOT = commands.Bot(command_prefix="&", description=DESCRIPTION)


__log__ = getLogger(__name__)


@BOT.event
async def on_ready():
    """Startup logged callout/setup"""
    __log__.info("logged in as: {}".format(BOT.user.id))


class ImageManipulation:
    """Image manipulation commands"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def primify(self, ctx: Context, shape_number: int = 25,
                      shape_type: str = "triangle", extra_shapes: int = 0):
        """Upload images and convert them to a primitive images

        .. note::

            You must run this command within the optional `add a comment`
            section while attaching/uploading images for this command to
            properly execute.

        The following image formats are supported by primitive-bot:
            - PNG
            - JPEG
            - JPG
            - GIF


        :param shape_number: The number of shapes to be used for constructing
            the primitive images.

            .. note::

                Due to computational limits shape_number must be equal or
                less than 200

        :type shape_number: int = 25


        :param shape_type: The type of shape to be used for constructing the
            primitive images. The following shape names ``OR`` shape reference
            numbers are allowed as arguments:
                - combo          ``OR``  0
                - triangle       ``OR``  1
                - rect           ``OR``  2
                - ellipse        ``OR``  3
                - circle         ``OR``  4
                - rotatedrect    ``OR``  5
                - beziers        ``OR``  6
                - rotatedellipse ``OR``  7
                - polygon        ``OR``  8
        :type shape_type: str = "triangle"


        :param extra_shapes: Add N extra shapes each iteration with
            reduced search (mostly good for beziers).

            .. note::

                Due to computational limits `extra_shapes` must be equal or
                less than 20

        :type extra_shapes: int = 0
        """
        for attachment in ctx.message.attachments:
            try:
                primitive_image, display_image = primify_attachment(
                    attachment=attachment,
                    shape_number=shape_number,
                    shape_type=shape_type,
                    extra_shapes=extra_shapes
                )
                out_id = uuid4()
                await self.bot.send_file(
                    ctx.message.channel,
                    fp=display_image,
                    filename="{}.png".format(out_id)
                )
                await self.bot.send_file(
                    ctx.message.channel,
                    fp=primitive_image,
                    filename="{}.svg".format(out_id)
                )
            except (ValueError, TypeError) as error:
                __log__.exception("failed to primify attachments", exc_info=True)
                await self.bot.send_message(
                    ctx.message.channel,
                    "ERROR: {}".format(error)
                )


BOT.add_cog(ImageManipulation(BOT))
