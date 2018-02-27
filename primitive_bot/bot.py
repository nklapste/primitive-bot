#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""primitive-bot Discord bot api"""

from logging import getLogger

from discord.ext import commands
from discord.ext.commands import Bot
from primitive_bot.images import download_image_attachments, primify_images

DESCRIPTION = """primitive-bot a Discord bot that converts inputted images
into primitive vector based graphics."""


BOT = commands.Bot(command_prefix="&", description=DESCRIPTION)


__log__ = getLogger(__name__)


@BOT.event
async def on_ready():
    """Startup logged callout/setup"""
    __log__.info("logged in as: {}".format(BOT.user.id))

# TODO Remove using for doc access
from discord.ext.commands.context import Context
from discord import Message

class ImageManipulation:
    """Image manipulation commands"""
    def __init__(self, bot: Bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def upload_image(self, ctx: Context, shape_number: int):
        """upload an image into a temporary instance for later editing"""
        images = download_image_attachments(ctx.message.attachments)

        primitive_images = primify_images(images, shape_number)

        for primitive_image in primitive_images:
                await self.bot.send_file(
                    ctx.message.channel,
                    fp=primitive_image,
                    filename="out.png"
                )


class Config:
    """Config commands for the primitive-bot"""

    def __init__(self, bot):
        self.bot = bot


BOT.add_cog(Config(BOT))

BOT.add_cog(ImageManipulation(BOT))
