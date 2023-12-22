from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, CommandHandler, ConversationHandler, Filters
import logging
from Token import TOKEN
from db import *
state = 0
subject = {"name": "", "surname": "", "birthdate": 0}
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


WAIT_NAME, WAIT_SURNAME, WAIT_BIRTHDAY, WAIT_YES_NO = range(4)


def ask_name(update: Update, context: CallbackContext, skipper = True):
    logger.info("ask_name")
    if isInDbById(update.effective_user.id) and skipper:
        context.bot.sendMessage(update.effective_user.id, f'Ваши данные уже есть в базе данных,'
                                                          f' {" ".join(find_by_id(update.effective_user.id))}.'
                                                          f' Вы хотите перезаписать данные? Напишите "да" или "нет"')
        return WAIT_YES_NO
    #global state
    #state = 1
    update.message.reply_text("ИМЯ!")
    return WAIT_NAME


def ask_sur(update: Update, context: CallbackContext):
    logger.info("ask_sur")
    global state
    #state = 2
    update.message.reply_text("ФАМИЛИЯ!")
    return WAIT_SURNAME


def ask_bd(update: Update, context: CallbackContext):
    logger.info("ask_bd")
    global state
    #state = 3
    update.message.reply_text("ДАТА РОЖДЕНИЯ!")
    return WAIT_BIRTHDAY


def get_answer(update: Update, context: CallbackContext):
    logger.info("get_answer")
    ans = update.message.text
    if ans == "да":
        return ask_name(update, context, False)
    context.bot.sendMessage(update.effective_user.id, 'Регистрация отменена')
    return ConversationHandler.END


def get_name(update: Update, context: CallbackContext):
    logger.info("get_name")
    global subject
    name = update.message.text
    context.user_data["name"] = name
    return ask_sur(update, context)


def get_sur(update: Update, context: CallbackContext):
    logger.info("get_sur")
    global subject
    sur = update.message.text
    context.user_data["surname"] = sur
    return ask_bd(update, context)


def get_bd(update: Update, context: CallbackContext):
    logger.info("get_bd")
    global subject
    bd = update.message.text
    context.user_data["birthdate"] = bd
    if not isInDbById(update.effective_user.id):
        write_to_bd([str(update.effective_user.id), context.user_data["name"], context.user_data["surname"], context.user_data["birthdate"]])
        update.message.reply_text(f'{context.user_data["name"]} {context.user_data["surname"]} с датой рождения {context.user_data["birthdate"]}, вы зарегистрированы в базе данных.')
    else:
        update.message.reply_text(f'Ваши данные были перезаписаны, {" ".join(find_by_id(update.effective_user.id)[1:3])} с датой рождения {find_by_id(update.effective_user.id)[3]} заменено на {context.user_data["name"]} {context.user_data["surname"]} с датой рождения {context.user_data["birthdate"]}')
        redact_by_id(update.effective_user.id, [str(update.effective_user.id), context.user_data["name"], context.user_data["surname"], context.user_data["birthdate"]])
    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', ask_name)],
    states={
        WAIT_NAME: [MessageHandler(Filters.text, get_name)],
        WAIT_SURNAME: [MessageHandler(Filters.text, get_sur)],
        WAIT_BIRTHDAY: [MessageHandler(Filters.text, get_bd)],
        WAIT_YES_NO: [MessageHandler(Filters.text, get_answer)]
    },
    fallbacks=[]
)


stateFunction = {1: get_name, 2: get_sur, 3: get_bd}


def main_handler(update: Update, context: CallbackContext):
    stateFunction[state](update, context)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), main_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CommandHandler("start", ask_name))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()