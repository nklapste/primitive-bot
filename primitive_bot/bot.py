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
    async def primify(self, ctx: Context, shape_number: int):
        """Upload an image and convert it to a primitive image"""
        for attachment in ctx.message.attachments:
            try:
                primitive_image, display_image = primify_attachment(
                    attachment=attachment,
                    shape_number=shape_number
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
