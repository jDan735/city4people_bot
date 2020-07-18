import telebot

with open("./token.txt") as token:
    bot = telebot.TeleBot(token.read())
    
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Я бот для определения кандидатов в вашем городе"
