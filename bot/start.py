from .__init__ import dp


@dp.message_handler(commands=["start"])
async def start(message):
    await message.reply("✋ *Привет!* Я бот для определения кандидатов в вашем городе \n\n⚙️ Команды:\n/start — выводит это окно\n- /form — присылает форму для оформления заявки на подписи\n/posts — присылает посты с сайта ГорПроектов\n- /city — определяет кандидата по вашему адресу\n\n👨🏻‍💻 Разработчик: [@jDan734](tg://?id=795449748)", parse_mode="Markdown")
