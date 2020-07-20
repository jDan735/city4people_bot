#!/usr/bin/env python

import telebot
import re
import os
import requests
from bs4 import BeautifulSoup

if "TOKEN_HEROKU" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN_HEROKU"])

elif "TOKEN" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN"])

else:
    with open("./token.txt") as token:
        bot = telebot.TeleBot(token.read())

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

urllist = {
    "tram": {
        "posts": "https://city4people.ru/posts/tag/%D1%82%D1%80%D0%B0%D0%BC%D0%B2%D0%B0%D0%B9",
        "postslist": []
    },
    "trolley": {
        "posts": "https://city4people.ru/posts/tag/%D1%82%D1%80%D0%BE%D0%BB%D0%BB%D0%B5%D0%B9%D0%B1%D1%83%D1%81",
        "postslist": []
    },
    "zero_deaths": {
        "posts": "https://city4people.ru/posts/tag/vision+zero",
        "postslist": []
    },
    "bicycles": {
        "posts": "https://city4people.ru/posts/tag/%D0%B2%D0%B5%D0%BB%D0%BE%D1%81%D0%B8%D0%BF%D0%B5%D0%B4%D1%8B",
        "postslist": []
    },
    "walkers": {
        "posts": "https://city4people.ru/posts/tag/%D0%BF%D0%B5%D1%88%D0%B5%D1%85%D0%BE%D0%B4%D1%8B",
        "postslist": []
    },
    "all_posts": {
        "posts": "https://city4people.ru/posts",
        "postslist": []
    },
}

status = {}

# ================================================================================================

def getPosts(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html.parser')
    list = []

    for row in soup.find_all("div", class_="col-lg-6"):
        try:
            list.append({
                "title": row.find("div", class_="project-item").h3.a.get_text(),
                "url": row.find("div", class_="project-item").h3.a.get("href")
            })
        except:
            pass

    for row in soup.find_all("div", class_="col-lg-4"):
        try:
            list.append({
                "title": row.find("div", class_="project-item").h3.a.get_text(),
                "url": row.find("div", class_="project-item").h3.a.get("href")
            })
        except:
            pass

    return list


# ======================= Проверка postslist ============================
vars = ["tram", "trolley", "zero_deaths", "bicycles", "walkers", "all_posts"]
for var in vars:
    urllist[var]["postslist"] = getPosts(urllist[var]["posts"])
    print("Load " + var)
# =======================================================================



# urllist["трамвай"]["postslist"] = getPosts(urllist["трамвай"]["posts"])

# ============================================================================================

@bot.message_handler(commands=["start"])
def start(message):
    status[message.chat.id] = {}
    bot.send_message(message.chat.id, "Привет! Я бот для определения кандидатов в вашем городе\n\nКоманды:\n/form - форма для оформления подписи")

@bot.message_handler(commands=["posts"])
def posts(message):

    if message.chat.type == "private":

        keyboard = telebot.types.InlineKeyboardMarkup()

        keyboard.add(telebot.types.InlineKeyboardButton(text="Трамвай", callback_data="tram"),
                     telebot.types.InlineKeyboardButton(text="Троллейбусы", callback_data="trolley"))

        keyboard.add(telebot.types.InlineKeyboardButton(text="Ноль смертей", callback_data="zero_deaths"),
                     telebot.types.InlineKeyboardButton(text="Велосипеды", callback_data="bicycles"))

        keyboard.add(telebot.types.InlineKeyboardButton(text="Пешеходы", callback_data="walkers"),
                     telebot.types.InlineKeyboardButton(text="Все", callback_data="all_posts"))
        #keyboard.row(telebot.types.InlineKeyboardButton(text="Нет", callback_data="no"))

        bot.send_message(message.chat.id, text="Выберите тег статей, пожалуйста", reply_markup=keyboard)

    else:
        #bot.send_message(message.chat.id, "Оформление подписи доступно только в личной переписке с ботом")
        bot.reply_to(message, "Чтение постов доступно только в личной переписке с ботом")

    # bot.reply_to(message, url["postslist"][0]["title"])

@bot.message_handler(commands=["form"])
def form(message):
    #bot.send_message(message.chat.id, "Для того, чтобы оставить подпись вам нужно указать:\n\n*Персональную информацию:*\n1. ФИО.\n2. Дату рождения (ДД.ММ.ГГГГ).\n3. Ваш адрес регистрации по паспорту, улица и номер дома.\n\n*Активные контакты:*\n1. Телефон.\n2. Электронную почту.", parse_mode="Markdown")

    if message.chat.type == "private":
        status[message.chat.id] = {}
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

    print(call.data)

    if call.data in urllist:
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass

        keyboard = telebot.types.InlineKeyboardMarkup()

        if "postlist" in urllist[call.data]:
            pass
        else:
            urllist[call.data]["postslist"] = getPosts(urllist[call.data]["posts"])

        for post in urllist[call.data]["postslist"][:10]:
            keyboard.add(telebot.types.InlineKeyboardButton(text=post["title"],
                    callback_data="TG_POST_ID=" + str(urllist[call.data]["postslist"].index(post)) + "," + call.data))

        bot.send_message(call.message.chat.id, "Выберите статью", reply_markup=keyboard)

    if re.match("TG_POST_ID=", call.data):
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass
        call.data = call.data.replace("TG_POST_ID=", "")
        data = call.data.split(",")
        bot.send_message(call.message.chat.id, "https://city4people.ru" + urllist[data[1]]["postslist"][int(data[0])]["url"])

    for city in cities:
        if len(city) == 2:
            for city1 in city:
                if call.data == city1:
                    try:
                        bot.delete_message(call.from_user.id, call.message.message_id)
                    except:
                        pass

                    status[call.message.chat.id]["city"] = city1
                    status[call.message.chat.id]["write_fio"] = True

                    bot.send_message(call.message.chat.id, "Хорошо. Ваш город *" + city[0] + "*. Напишите ваше ФИО", parse_mode="Markdown")

        elif len(city) == 1:
            if call.data == city[0]:
                try:
                    bot.delete_message(call.from_user.id, call.message.message_id)
                except:
                    pass

                status[call.message.chat.id]["city"] = city[0]
                status[call.message.chat.id]["write_fio"] = True

                bot.send_message(call.message.chat.id, "Хорошо. Ваш город *" + city[0] + "*. Напишите ваше ФИО", parse_mode="Markdown")

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
        status[message.chat.id]["write_fio"] = True
    elif call.data == "no_form":
        try:
            bot.delete_message(call.from_user.id, call.message.message_id)
        except:
            pass

        bot.send_message(call.message.chat.id, "Хорошо. Отменяю запрос")

@bot.message_handler(content_types = ["text"])
def text(message):
    if message.chat.id > 0:

        #=============================================== Writing statuses ==========================================

        if status[message.chat.id]["write_fio"]:
            if re.match(r"[а-яА-Я]{1,}\s[а-яА-Я]{1,}\s[а-яА-Я]{1,}", message.text):
                status[message.chat.id]["write_birthday"] = True
                status[message.chat.id]["write_fio"] = False

                status[message.chat.id]["subname"] = message.text.split(" ", 1)[0],
                status[message.chat.id]["name"] = message.text.split(" ", 1)[1].split(" ", 1)[0],
                status[message.chat.id]["middle_name"] = message.text.split(" ", 1)[1].split(" ", 1)[1].split(" ", 1)

                # bot.send_message(message.chat.id, status["subname"][0])
                # bot.send_message(message.chat.id, status["name"][0])
                # bot.send_message(message.chat.id, status["middle_name"][0])
                # bot.send_message(message.chat.id, "Ваша фамилия - *" + str(status["subname"][0]) + "*\nВаше имя - *" + str(status["name"][0]) + "*\nВаше отчество - *" + str(status["middle_name"][0]) + "*", parse_mode="Markdown")
                bot.reply_to(message, "Напишите вашу дату рождения (ДД.ММ.ГГГГ)")
                # except:
                #     bot.reply_to(message, "Некорректные данные")
            else:
                bot.send_message(message.chat.id, "ФИО написано не правильно")

        elif status[message.chat.id]["write_birthday"]:
            if re.match(r"[0-3]\d\.[0-1]\d\.[1-2]\d{3}", message.text):

                status[message.chat.id]["birthday"] = message.text

                bot.reply_to(message, "Отправьте ваш адрес регистрации *по паспорту*, улицу и номер дома.\n\n_(Поставить подпись за кандидата возможно, если ваш адрес в избирательном округе кандидата)_", parse_mode="Markdown")

                status[message.chat.id]["write_birthday"] = False
                status[message.chat.id]["write_fio"] = False
                status[message.chat.id]["write_place"] = True
            else:
                bot.reply_to(message, "Данные некорректные, введите снова")

        elif status[message.chat.id]["write_place"]:
            if message.text:

                status[message.chat.id]["place"] = message.text

                bot.send_message(message.chat.id, "Данные не проверял, верю наслово, на сервере их тоже не храню — места нет. Отправьте ваш адрес электронной почты")

                status[message.chat.id]["write_place"] = False
                status[message.chat.id]["write_email"] = True

        elif status[message.chat.id]["write_email"]:
            if re.match(r".{1,}@.{1,}", message.text):

                status[message.chat.id]["email"] = message.text

                bot.send_message(message.chat.id, "Теперь напишите ваш номер телефона (*+7*_xxxxxxxxx_)", parse_mode="Markdown")

                status[message.chat.id]["write_place"] = False
                status[message.chat.id]["write_email"] = False
                status[message.chat.id]["write_phone"] = True
            else:
                bot.send_message(message.chat.id, "Отправьте адрес электронной почты снова")

        elif status[message.chat.id]["write_phone"]:
            if re.match(r"\+7\d{9}", message.text):

                status[message.chat.id]["phone"] = message.text

                bot.send_message(message.chat.id, "Теперь вы можете отправить заявку :)", parse_mode="Markdown")

                #bot.send_message(message.chat.id, "Фамилия - *" + status[message.chat.id]["subname"][0] + "*\n" +
                #                                  "Имя - *" + status[message.chat.id]["name"][0] + "*\n" +
                #                                  "Отчество - *" + status[message.chat.id]["middle_name"][0] + "*\n" +
                #                                  "День Рождения - *" + status[message.chat.id]["birthday"] + "*\n" +
                #                                  "Город - *" + status[message.chat.id]["city"] + "*\n" +
                #                                  "Место - *" + status[message.chat.id]["place"] + "*\n" +
                #                                  "Почта - *" + status[message.chat.id]["email"] + "*\n" +
                #                                  "Номер телефона - *" + status[message.chat.id]["phone"] + "*",
                #                                  parse_mode="Markdown")

                status[message.chat.id]["write_place"] = False
                status[message.chat.id]["write_email"] = False
                status[message.chat.id]["write_phone"] = False

            else:
                bot.send_message(message.chat.id, "Введите правильный номер")

        # else:
        #     bot.reply_to(message, "Я еще не умею работать с текстом")

bot.polling()
