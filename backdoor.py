ADMINS = ["TolstovViktor"]
from db import reader

def database_send(update, context):
    username = update.effective_user.username
    if username not in ADMINS:
        context.bot.send_message(update.effective_user.id, "0 + 0 = 0")
        return
    with reader() as file:
        context.bot.send_message(update.effective_user.id, f"{file.read()}")