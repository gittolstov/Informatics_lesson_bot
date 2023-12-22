from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from random import random
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler, CallbackQueryHandler
import logging
from Token import TOKEN
from AnketaListenerBot import register_handler
import backdoor
global_keyboard = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
whitelist = ["kolodezhv", "TolstovViktor", "dim_akim", "httzff"]
database = ""


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

base_url = "https://api.telegram.org/bot"
end_url = "/getMe"
url = f"{base_url}{TOKEN}{end_url}"


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
            num2 = float(txt[i + 1:len(txt)])
            num1 = float(txt[0:i])
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
    update.message.reply_text(f"{ident}, здравствуйте, я бот [*insert bot name*]."
                              f"\n Я обладаю широким спектром бесполезных или частично бесполезных функций."
                              f"\nНапишите /help для получения списка возможностей."
                              f"\nОсновной функцией является вычисление арифметических выражений формата <a><операция><б>"
                              f"\nПоддерживаются операции деления (/), умножения, (*), вычитания (-) и сложения (+).")
    logger.info(f"Acquired username of {ident}")
    global database
    if ident not in database:
        database.join(f"{ident}, ")
    logger.info(update.effective_user.id)
    logger.info("message sent")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Поддерживаемые команды:\n<i>/start</i>\n<i>/help</i>\n<i>/keyboard</i> (вызывает клавиатуру в сообщении для запуска таймера)"
                              "\n<i>/keyboard2</i> (вызывает клавиатуру в поле ввода для вычисления квадратов чисел от 0 до 9)\n<i>/clear</i> (выключает таймер)"
                              "\n<i>/register</i> (регистрирует пользователя в базе данных, если пользователь уже зарегистрирован,"
                              " данные будут перезаписаны и старые данные выведены на экран)", parse_mode=ParseMode.HTML)
    logger.info("helped")


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
    update.message.reply_text("Установите таймер", reply_markup=keyboard)


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
    set_timer(update, context, data[0])
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
        ["1 * 1", "2 * 2", "3 * 3"],
        ["4 * 4", "5 * 5", "6 * 6"],
        ["7 * 7", "8 * 8", "9 * 9"],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text("Вычислите квадрат числа", reply_markup=keyboard)
    logger.info("Keyboard created")


def v1_text(update: Update, context: CallbackContext):
    if vlad_protection(update):
        return
    update.message.reply_text(f"{bin(int(random() * 256))}"[2:8])
    logger.info(f"JUDGEMENT")


def set_timer(update: Update, context: CallbackContext, time):
    clear(update, context)
    logger.info(f"timer set for {time} seconds")
    context.bot.sendMessage(update.effective_user.id, f"Запущен таймер с периодом {time} секунд.\nНажмите /clear чтобы остановить.")
    context.bot_data["user_idi"] = update.effective_user.id
    context.bot_data["xx"] = 0
    context.bot_data["x"] = time
    context.bot_data["job"] = context.job_queue.run_repeating(show_seconds, time)


def show_seconds(context: CallbackContext):
    context.bot.sendMessage(context.bot_data["user_idi"], context.bot_data["xx"])
    context.bot_data["xx"] += context.bot_data["x"]


def clear(update: Update, context: CallbackContext):
    for job in context.job_queue.jobs():
        job.schedule_removal()
    logger.info("timers cleared")
    context.bot.sendMessage(update.effective_user.id, "Все таймеры очищены")


def vlad_protection(update: Update):
    for i in whitelist:
        if update.effective_user.username == i:
            return False
    update.message.reply_text("ХРЕН вам")
    logger.info(f"restricted user! {update.effective_user.username}")
    return True


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    command_list = ["start", "prepare_thyself", "keyboard", "keyboard2", "help", "clear", "amogus_bogus"]
    function_list = [start, v1_text, inline_keyboard, keyboard_handler, help, clear, backdoor.database_send]
    for i in range(len(command_list)):
        dispatcher.add_handler(CommandHandler(command_list[i], function_list[i]))
    echo_handler = MessageHandler(Filters.text & (~Filters.command), calculate)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CallbackQueryHandler(inline_keyboard_button_handler))
    updater.start_polling()
    updater.idle()


main()
jeong = 1630691854