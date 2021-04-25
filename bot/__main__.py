from aiogram import executor

from .start import start
from .posts import posts
from .__init__ import dp

import asyncio
import logging
import coloredlogs


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

executor.start_polling(dp, loop=loop)
