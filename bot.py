from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from random import random
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, CallbackQueryHandler
import logging
from Token import TOKEN
global_keyboard = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
blacklist = ["kolodezhv", "TolstovViktor"]

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
    if vlad_protection(update):
        return
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
    update.message.reply_text(f"{num1} {operation} {num2} = {res}.\n", reply_markup=ReplyKeyboardRemove())
    logger.info(f"user {usr} calculated {num1} {operation} {num2}")


def start(update: Update, context: CallbackContext):
    if vlad_protection(update):
        return
    ident = update.message.from_user.username
    update.message.reply_text(f"{ident}, твой айпи-адрес уже у меня. Скоро я тебя вычислю!")
    logger.info(f"Acquired username of {ident}")
    global database
    if ident not in database:
        database.join(f"{ident}, ")


def inline_keyboard(update: Update, context: CallbackContext):
    if vlad_protection(update):
        return
    buttons = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
    for a in range(len(buttons)):
        for b in range(len(buttons[a])):
            buttons[a][b] = InlineKeyboardButton(text=buttons[a][b], callback_data=f"{buttons[a][b]}_{a}_{b}")
    keyboard = InlineKeyboardMarkup(buttons)
    logger.info("Inline keyboard created")
    update.message.reply_text("Choose wisely"
                              "<b>\nsemi-bald</b>"
                              "<i>\nabobe</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML)


def inline_keyboard_button_handler(update: Update, context: CallbackContext):
    if vlad_protection(update):
        return
    global global_keyboard
    query = update.callback_query
    '''markup = query.message.reply_markup
    logger.info(markup)
    keyboard = markup.inline_keyboard
    logger.info(keyboard)
    data = query.data.split("_")
    for i in data:
        i = int(i)
    logger.info(markup[data[1]][data[2]])
    keyboard[int(data[1])][int(data[2])] = InlineKeyboardButton(text=data[0], callback_data=f"{int(data[0]) + 1}_{data[1]}_{data[2]}")'''
    data = query.data.split("_")
    for i in range(len(data)):
        data[i] = int(data[i])
    logger.info(global_keyboard[data[1]][data[2]])
    logger.info(int(global_keyboard[data[1]][data[2]]) + 1)
    global_keyboard[data[1]][data[2]] = str(int(global_keyboard[data[1]][data[2]]) + 1)
    logger.info(global_keyboard[data[1]][data[2]])
    buttons = [global_keyboard[0].copy(), global_keyboard[1].copy(), global_keyboard[2].copy()]
    for a in range(len(buttons)):
        for b in range(len(buttons[a])):
            buttons[a][b] = InlineKeyboardButton(text=buttons[a][b], callback_data=f"{buttons[a][b]}_{a}_{b}")
    keyboard = InlineKeyboardMarkup(buttons)
    logger.info(keyboard)
    query.edit_message_reply_markup(keyboard)


def keyboard_handler(update: Update, context: CallbackContext):
    buttons = [
        ["один", "два", "три"],
        ["четыре", "пять", "шесть"],
        ["семь", "восемь", "одиннадцать"],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text("Choose wisely", reply_markup=keyboard)
    logger.info("Keyboard created")


def v1_text(update: Update, context: CallbackContext):
    if vlad_protection(update):
        return
    update.message.reply_text(f"{bin(int(random() * 256))}"[2:8])
    logger.info(f"JUDGEMENT")


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    command_list = ["start", "prepare_thyself", "keyboard"]
    function_list = [start, v1_text, inline_keyboard]
    for i in range(len(command_list)):
        dispatcher.add_handler(CommandHandler(command_list[i], function_list[i]))
    echo_handler = MessageHandler(Filters.text & (~Filters.command), calculate)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_button_handler))
    updater.start_polling()
    updater.idle()


def vlad_protection(update: Update):
    for i in blacklist:
        if update.effective_user.username == i:
            update.message.reply_text("ХРЕН вам")
            logger.info(f"restricted user! {update.effective_user.username}")
            return True
    return False

main()
