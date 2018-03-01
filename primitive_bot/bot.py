#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""primitive-bot Discord bot api"""

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
    async def upload_image(self, ctx: Context, shape_number: int):
        """upload an image into a temporary instance for later editing"""
        for attachment in ctx.message.attachments:
            await self.bot.send_file(
                ctx.message.channel,
                fp=primify_attachment(
                    attachment=attachment,
                    shape_number=shape_number
                ),
                filename="out.svg"
            )


class Config:
    """Config commands for the primitive-bot"""

    def __init__(self, bot):
        self.bot = bot


BOT.add_cog(Config(BOT))

BOT.add_cog(ImageManipulation(BOT))
