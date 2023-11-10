from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, CommandHandler, ConversationHandler, Filters
import logging
from Token import TOKEN
state = 0
subject = {"name": "", "surname": "", "birthdate": 0}
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def ask_name(update: Update, context: CallbackContext):
    logger.info("ask_name")
    global state
    state = 1
    update.message.reply_text("ИМЯ!")


def ask_sur(update: Update, context: CallbackContext):
    logger.info("ask_sur")
    global state
    state = 2
    update.message.reply_text("ФАМИЛИЯ!")


def ask_bd(update: Update, context: CallbackContext):
    logger.info("ask_bd")
    global state
    state = 3
    update.message.reply_text("ДАТА РОЖДЕНИЯ!")


def get_name(update: Update, context: CallbackContext):
    logger.info("get_name")
    global subject
    name = update.message.text
    subject["name"] = name
    ask_sur(update, context)

def get_sur(update: Update, context: CallbackContext):
    logger.info("get_sur")
    global subject
    sur = update.message.text
    subject["surname"] = sur
    ask_bd(update, context)


def get_bd(update: Update, context: CallbackContext):
    logger.info("get_bd")
    global subject
    bd = update.message.text
    subject["birthdate"] = bd
    print(subject["name"], subject["surname"], subject["birthdate"])


#register_handler = ConversationHandler(
#    entry_points=[CommandHandler("register", ask_name)]
#)


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


main()