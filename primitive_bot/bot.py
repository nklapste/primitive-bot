#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""primitive-bot Discord bot api"""

from logging import getLogger

from discord.ext import commands


DESCRIPTION = """primitive-bot a Discord bot that converts inputted images
into primitive vector based graphics."""


BOT = commands.Bot(command_prefix="&", description=DESCRIPTION)


__log__ = getLogger(__name__)


@BOT.event
async def on_ready():
    """Startup logged callout/setup"""
    __log__.info("logged in as: {}".format(BOT.user.id))


class Config:
    """Config commands for the primitive-bot"""

    def __init__(self, bot):
        self.bot = bot


BOT.add_cog(Config(BOT))
