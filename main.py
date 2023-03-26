from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import openai
from dotenv import load_dotenv
import os
import config

# import command handlers
from commands import (
    handle_command_start,
    handle_command_help,
    handle_command_error,
    handle_command_timeout,
    handle_command_reset
)

# import error handler
from error import handle_error

# import message handlers
from handlers import (
    handle_message_text,
    handle_message_voice
)

# import callback query handler
from callbackquery import handle_callback_query


load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


logging = config.logging


def main():
    logging.info("Starting GenieGPT")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add the command handlers
    dispatcher.add_handler(CommandHandler('start', handle_command_start))
    dispatcher.add_handler(CommandHandler('help', handle_command_help))
    dispatcher.add_handler(CommandHandler('error', handle_command_error))
    dispatcher.add_handler(CommandHandler('timeout', handle_command_timeout))
    dispatcher.add_handler(CommandHandler('reset', handle_command_reset))

    # add the text message hadler
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), handle_message_text))

    # add the voice note handler
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_message_voice))

    # add the error handler to dispatcher
    dispatcher.add_error_handler(handle_error)

    # add the callbackquery handler - this function defines what happenes when one of the inline buttons gets pressed
    dispatcher.add_handler(CallbackQueryHandler(handle_callback_query))

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
