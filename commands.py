import config
import telegram
import openai
from telegram.ext import CommandHandler
from config import WELCOME_MESSAGE

logging = config.logging


def handle_command_start(update, context):
    """Start the bot"""
    update.message.reply_text(text=WELCOME_MESSAGE,
                              parse_mode=telegram.ParseMode.MARKDOWN)


# define a function to raise errors
def handle_command_error(update, context):
    """a special command for debugging, raises an EnvironmentError"""
    raise EnvironmentError


def handle_command_timeout(update, context):
    raise openai.error.Timeout


def handle_command_help(update, context):
    """Get the list of all commands available"""
    logging.info("Entering help_command")
    # Get the list of registered command handlers from the dispatcher
    logging.info("Printing all handlers:")
    logging.info(context.dispatcher.handlers[0])
    handlers = context.dispatcher.handlers[0]
    command_handlers = [handler for handler in handlers if isinstance(handler, CommandHandler)]
    logging.info("Printing command handlers:")
    logging.info(command_handlers)
    commands = [command_handler.command for command_handler in command_handlers]
    logging.info("Printing commands:")
    logging.info(commands)
    help_msg = f'*Here is the list of available commands:*\n\n'

    for command_handler in command_handlers:
        for command in command_handler.command:
            help_msg += f"/{command} - {command_handler.callback.__doc__ or 'no description 🙁'}\n\n"

    # Send the help message to the user
    logging.info(f"Constructed help message")
    logging.info(help_msg)
    update.message.reply_text(text=help_msg, parse_mode=telegram.ParseMode.MARKDOWN)
    logging.info("Exiting help command")

