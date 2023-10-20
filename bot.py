import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import random
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler
import logging
from Token import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
database = ""

base_url = "https://api.telegram.org/bot"
end_url = "/getMe"
url = f"{base_url}{TOKEN}{end_url}"


def do_echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(f"Сам ты {text}")


def calculate(update: Update, context: CallbackContext):
    operation = "+"
    txt = update.message.text
    usr = update.message.from_user.username
    num1 = 0
    num2 = 0
    for i in range(len(txt)):
        if txt[i] == "+" or txt[i] == "-" or txt[i] == "*" or txt[i] == "/":
            operation = txt[i]
            num2 = int(txt[i + 1:len(txt)])
            num1 = int(txt[0:i])
    res = 0
    if operation == "+":
        res = num1 + num2
    elif operation == "-":
        res = num1 - num2
    elif operation == "*":
        res = num1 * num2
    elif operation == "/":
        res = num1 / num2
    update.message.reply_text(f"{num1} {operation} {num2} = {res}.\n")
    logger.info(f"user {usr} calculated {num1} {operation} {num2}")


def start(update: Update, context: CallbackContext):
    ident = update.message.from_user.username
    update.message.reply_text(f"{ident}, твой айпи-адрес уже у меня. Скоро я тебя вычислю!")
    logger.info(f"Acquired username of {ident}")
    global database
    if ident not in database:
        database.join(f"{ident}, ")


def keyboard_handler(update: Update, context: CallbackContext):
    buttons = [
        ["один", "два", "три"],
        [ "четыре", "пять", "шесть"],
        [ "семь", "восемь", "одиннадцать"],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text("Choose wisely", reply_markup=keyboard)


def v1_text(update: Update, context: CallbackContext):
    update.message.reply_text(f"{bin(int(random() * 256))}"[2:8])
    logger.info(f"JUDGEMENT")


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    start_handler = CommandHandler("prepare_thyself", v1_text)
    dispatcher.add_handler(start_handler)
    keyb_handler = CommandHandler("keyboard", keyboard_handler)
    dispatcher.add_handler(keyb_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), calculate)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    updater.idle()


main()
