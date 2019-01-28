import config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from image_recognition import PredictionThread

import wikipedia
import logging
import os

execution_path = os.getcwd()

wikipedia.set_lang("pt")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


cont = 0
phrases = [None, None, None, None]


# Create a new instance of a ChatBot
chat_bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)


trainer = ListTrainer(chat_bot)

trainer.train([
    "Oi",
    "Olá",
    "Tudo bem?",
    "Tudo bem sim, e com você?"
])


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Olá!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    global phrases
    global cont
    phrases[cont % 4] = update.message.text
    cont += 1
    if cont % 4 == 0:
        trainer.train(phrases)
    print(cont)


def nerd(bot, update):
    query = update.message.text.replace("/nerd", "")
    bot_response = chat_bot.get_response(query)
    update.message.reply_text(str(bot_response))


def wiki(bot, update):
    query = update.message.text.replace("/wiki", "")
    wiki_response = wikipedia.summary(query)
    update.message.reply_text(str(wiki_response))


def image(bot, update):
    file_id = update.message.photo[-1].file_id
    new_file = bot.get_file(file_id)
    new_file.download("image.jpeg")
    prediction_thread = PredictionThread()
    prediction_thread.start()
    prediction_thread.join()
    update.message.reply_text(prediction_thread.result)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():

    updater = Updater(config.TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("nerd", nerd))
    dp.add_handler(CommandHandler("wiki", wiki))

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, image))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
