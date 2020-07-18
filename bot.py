import telebot
import re

status = {
    "write_fio": False,
    "write_birthday": False
}

cities = [
    ["Владимир", "Воронеж"],
    ["Иваново", "Калуга"],
    ["Кастрома", "Краснодар"],
    ["Липецк", "Орел"],
    ["Самара", "Смоленск"],
    ["Сочи", "Томск"],
    ["Псковская область"],
    ["Нижний Новгород"],
    ["Ростов-на-Дону"]
]

with open("./token.txt") as token:
    bot = telebot.TeleBot(token.read())
    
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для определения кандидатов в вашем городе\n\nКоманды:\n/form - форма для оформления подписи")

@bot.message_handler(commands=["form"])
def form(message):
    #bot.send_message(message.chat.id, "Для того, чтобы оставить подпись вам нужно указать:\n\n*Персональную информацию:*\n1. ФИО.\n2. Дату рождения (ДД.ММ.ГГГГ).\n3. Ваш адрес регистрации по паспорту, улица и номер дома.\n\n*Активные контакты:*\n1. Телефон.\n2. Электронную почту.", parse_mode="Markdown")
    if message.chat.type == "private":
        #bot.send_message(message.chat.id, "Для того, чтобы оставить подпись Вам нужно указать персональные данные, телефон, емайл, а также адрес регистрации по паспорту, улицу и номер дома")
        bot.reply_to(message, "Для того, чтобы оставить подпись Вам нужно указать персональные данные, телефон, электронную почту, а также адрес регистрации по паспорту, улицу и номер дома")

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="Да", callback_data="yes_form"), telebot.types.InlineKeyboardButton(text="Нет", callback_data="no_form"))
        #keyboard.row(telebot.types.InlineKeyboardButton(text="Нет", callback_data="no"))

        bot.send_message(message.chat.id, text="Продолжаем?", reply_markup=keyboard)

    else:
        #bot.send_message(message.chat.id, "Оформление подписи доступно только в личной переписке с ботом")
        bot.reply_to(message, "Оформление подписи доступно только в личной переписке с ботом")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    for city in cities:        
        if len(city) == 2:
            for city1 in city:
                if call.data == city1: 
                    try:
                        bot.delete_message(call.from_user.id, call.message.message_id)
                    except:
                        pass

                    status["city"] = city1
                    status["write_fio"] = True

                    bot.send_message(call.message.chat.id, "Хорошо. Ваш город *" + city1 + "*", parse_mode="Markdown")
                    bot.send_message(call.message.chat.id, "Напишите ваше ФИО.")

        elif len(city) == 1:
            if call.data == city[0]:    
                try:
                    bot.delete_message(call.from_user.id, call.message.message_id)
                except:
                    pass

                status["city"] = city[0]
                status["write_fio"] = True

                bot.send_message(call.message.chat.id, "Хорошо. Ваш город *" + city[0] + "*", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "Напишите ваше ФИО.")






    if call.data == "yes_form":
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass

        keyboard = telebot.types.InlineKeyboardMarkup()

        for city in cities:

            if len(city) == 1:
                keyboard.add(telebot.types.InlineKeyboardButton(text=city[0], callback_data=city[0]))

            if len(city) == 2:
                keyboard.add(telebot.types.InlineKeyboardButton(text=city[0], callback_data=city[0]), telebot.types.InlineKeyboardButton(text=city[1], callback_data=city[1]))

        bot.send_message(call.message.chat.id, "Выберите город", reply_markup=keyboard)        
    elif call.data == "select_fio":
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, "Напишите ваше ФИО.")
        status["write_fio"] = True
    elif call.data == "no_form":
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass

        bot.send_message(call.message.chat.id, "Хорошо. Отменяю запрос.")

@bot.message_handler(content_types = ["text"])
def text(message):
    if status["write_fio"]:
        status["write_birthday"] = True
        status["write_fio"] = False

        status["name"] = message.text.split(" ", 1)[0],
        status["subname"] = message.text.split(" ", 1)[1].split(" ", 1)[0],
        status["middle_name"] = message.text.split(" ", 1)[1].split(" ", 1)[1].split(" ", 1)[0]

        bot.send_message(message.chat.id, status["subname"])
        bot.send_message(message.chat.id, status["name"])
        bot.send_message(message.chat.id, status["middle_name"])
        bot.send_message(message.chat.id, "Ваша фамилия - *" + status["subname"] + "*.\nВаше имя - *" + status["name"] + "*\nВаше отчество - *" + status["middle_name"] + "*", parse_mode="Markdown")
        bot.reply_to(message, "Напишите вашу дату рождения (ДД.ММ.ГГГГ)")
        # except:
        #     bot.reply_to(message, "Некорректные данные")

    elif status["write_birthday"]:
        if re.match(r"[0-3]\d\.[0-1]\d\.[1-2]\d{3}", message.text):
            bot.reply_to(message, "Отправьте ваш адрес регистрации *по паспорту*, улицу и номер дома.\n\n_Поставить подпись за кандидата возможно, если ваш адрес в избирательном округе кандидата_", parse_mode="Markdown")
            status["write_birthday"] = False
        else:
            bot.reply_to(message, "Данные некорректные, введите снова")

    else:       
        bot.reply_to(message, "Я еще не умею работать с текстом")

bot.polling()


