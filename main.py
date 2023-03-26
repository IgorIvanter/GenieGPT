from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import telegram
import openai
from dotenv import load_dotenv
import os
import config


# import commands
from commands import handle_command_help
from commands import handle_command_start
from commands import handle_command_timeout
from commands import handle_command_error

# import error handler
from error import handle_error

# import message handlers
from handlers import handle_message_text
from handlers import handle_message_voice


load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


logging = config.logging


def button_callback_retry(update, context):
    last_request = context.user_data.get("last_request")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"*[You]:* {last_request}",
                             parse_mode=telegram.ParseMode.MARKDOWN)
    last_error_message = context.user_data['last_error_message']
    context.bot.edit_message_text(chat_id=last_error_message.chat.id,
                                  message_id=last_error_message.message_id, text=last_error_message.text)
    last_update = context.user_data['last_update']
    handle_message_text(last_update, context)


def handle_callback_query(update, context):
    query = update.callback_query
    query.answer()
    button_id = query.data
    if button_id == 'retry':
        button_callback_retry(update, context)
    else:
        query.edit_message_text(text="Invalid button")


def main():
    logging.info("Starting GenieGPT")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add the command handlers
    dispatcher.add_handler(CommandHandler('start', handle_command_start))
    dispatcher.add_handler(CommandHandler('help', handle_command_help))
    dispatcher.add_handler(CommandHandler('error', handle_command_error))
    dispatcher.add_handler(CommandHandler('timeout', handle_command_timeout))

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
