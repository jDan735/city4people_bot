from aiogram import types
from .__init__ import bot, dp, posts, post_cache

import yaml


POSTS_KEYS = [
    [["🚋 Трамвай", "tram"], ["🚎 Троллейбусы", "trolley"]],
    [["👩‍🚀 Ноль смертей", "zero_deaths"], ["🚲 Велосипеды", "bicycles"]],
    [["🚶 Пешеходы", "walkers"], ["🗂 Все", "all_posts"]]
]


tags_keyboard = types.InlineKeyboardMarkup()


for line in POSTS_KEYS:
    keys = [types.InlineKeyboardButton(text=key[0], callback_data=yaml.dump({
                "tag": key[1],
                "position": [0, 10]
            })) for key in line]

    tags_keyboard.add(*keys)


@dp.message_handler(commands=["posts"])
async def _posts(message):
    await message.reply("🏷 Выберите тег статей, пожалуйста",
                        reply_markup=tags_keyboard)


@dp.callback_query_handler(lambda call: 
                           yaml.safe_load(call.data)["tag"] in list(posts.URLS.keys()))
async def callback_posts(call):
    info = yaml.safe_load(call.data)

    if info.get("position") is None and info.get("post_id") is not None:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=post_cache[info["tag"]][info["post_id"]]["url"]
        )

        return

    back, next = tuple(info["position"])
    LIMIT = len(post_cache[info["tag"]])

    posts_keyboard = types.InlineKeyboardMarkup()

    for num, post in enumerate(post_cache[info["tag"]][back:next]):
        posts_keyboard.add(types.InlineKeyboardButton(
            text=post["name"],
            callback_data=yaml.dump({
                "tag": info["tag"],
                "post_id": num
            })
        ))

    navigation = []

    if back > 0:
        navigation.append(types.InlineKeyboardButton(
            text="👈 Назад",
            callback_data=yaml.dump({
                "tag": info["tag"],
                "position": [back - 10, next - 10] if back - 10 >= 0 else [back, next]
            })
        ))

    status = " / ".join([str(next), str(LIMIT)])
    navigation.append(types.InlineKeyboardButton(text=status,
                                                 callback_data="status"))

    if next < LIMIT:
        navigation.append(types.InlineKeyboardButton(
            text="Вперед 👉",
            callback_data=yaml.dump({
                "tag": info["tag"],
                "position": [back + 10, next + 10] if next + 10 < LIMIT else [back, LIMIT]
            })
        ))

    posts_keyboard.add(*navigation)


    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="🔎 Выберите статью",
                                reply_markup=posts_keyboard)
