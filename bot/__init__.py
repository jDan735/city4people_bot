from aiogram import Bot, Dispatcher

from os import environ
import yaml

from .cityapi import post_cache, posts


if "TOKEN" in environ:
    TOKEN = environ["TOKEN"]

else:
    with open("config.yml") as cfg:
        config = yaml.safe_load(cfg.read())
        TOKEN = config.get("token")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
