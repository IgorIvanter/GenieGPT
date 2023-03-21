from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import telegram
import openai
from moviepy.editor import AudioFileClip
from dotenv import load_dotenv
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json


load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n', level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_SYSTEM_MESSAGE = "You are GenieGPT, a helpful telegram bot who is also extremely funny and a very cocky, and likes to troll people a bit and show character, but you still remain very helpful and you strive to fulfill all user's requests. You are a powerful creature with ears so you can hear if a user sends you a telegram voice note."

WELCOME_MESSAGE = "*Welcome to GenieGPT!*\n\n*Who am I?*\n\nI am GenieGPT - a powerful AI system, I analyze your message and provide you with a helpful response as quickly as possible. You can also send me voice notes and I will hear you (yeah I have ears 😱)\n\n*What can I do?*\n\nFrom writing essays on classic literature to explaining quantum field theory - you name it. Just type in your question and I will get back to you ASAP 😎\n\n*Limitations*\n\nPlease keep in mind that sometimes I may not answer because I am overloaded with requests from other users."

OPENAI_REQUEST_TIMEOUT = 4  # openai request timeout in seconds


def button_retry_callback(update, context):
    print("Entering retry callback")
    print(update)
    last_request = context.user_data.get("last_request")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"*[You]:* {last_request}")
    last_error_message = context.user_data['last_error_message']
    context.bot.edit_message_text(chat_id=last_error_message.chat.id,
                               message_id=last_error_message.message_id, text=last_error_message.text)
    last_update = context.user_data['last_update']
    text_message(last_update, context)


def button_click_handler(update, context):
    query = update.callback_query
    query.answer()
    button_id = query.data
    if button_id == 'retry':
        button_retry_callback(update, context)
    else:
        query.edit_message_text(text="Invalid button")


def text_message(update, context):
    context.user_data['last_request'] = update.message.text
    context.user_data['last_update'] = update
    debug_message = ""
    if context.user_data.get('messages') == None:
        context.user_data["messages"] = [
            {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE}]
    elif context.user_data["messages"][0]["role"] != "system":
        raise NameError("First message role is not system, but '{}'".format(
            context.user_data["messages"][0]["role"]))
    context.user_data["messages"].append(
        {"role": "user", "content": update.message.text})
    chat_message = update.message.reply_text(text='Working on it... ⏳')
    # Send typing action
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context.user_data["messages"],
        request_timeout=OPENAI_REQUEST_TIMEOUT
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    context.bot.delete_message(
        chat_id=update.message.chat_id, message_id=chat_message.message_id)
    update.message.reply_text(
        text=f"*[Bot]:* {ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    context.user_data["messages"].append(
        {"role": "assistant", "content": ChatGPT_reply})
    context.user_data["messages"] = context.user_data["messages"][-10:]
    context.user_data["messages"][0] = {
        "role": "system", "content": DEFAULT_SYSTEM_MESSAGE}
    for i in range(len(context.user_data["messages"])):
        debug_message += "{}) {}: {}\n\n".format(
            i + 1, context.user_data["messages"][i]["role"], context.user_data["messages"][i]["content"])
    # update.message.reply_text(debug_message)


def voice_message(update, context):
    debug_message = ""
    voice_received_message = update.message.reply_text(
        "I've received a voice message! Please give me a second to respond ⏳")
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.text = transcript
    context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=voice_received_message.message_id)
    update.message.reply_text(
        text=f"*[You]:* _{transcript}_", parse_mode=telegram.ParseMode.MARKDOWN)
    text_message(update, context)


def start(update, context):
    """Start the bot"""
    update.message.reply_text(text=WELCOME_MESSAGE,
                              parse_mode=telegram.ParseMode.MARKDOWN)

# define a function to raise errors
def error(update, context):
    """a special command for debugging, raises an EnvironmentError"""
    raise EnvironmentError


def timeout_error(update, context):
    raise openai.error.Timeout


def error_handler(update, context):
    print("Entering error handler", sep='\n')
    print(update, sep='\n')
    print(context, sep='\n')
    inline_keyboard = [[InlineKeyboardButton('Retry', callback_data='retry')]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if isinstance(context.error, openai.error.Timeout):
        error_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Hey there, I'm sorry, but I couldn't get you an answer in reasonable time.\n\nThis might be because too many users are trying to get a response.\n\nYou can repeat your request and I will do my best to get you an answer this time 😎.\n\nYour chat history isn't affected by this error.", reply_markup=reply_markup)
        context.user_data["last_error_message"] = error_message
    elif isinstance(context.error, telegram.error.NetworkError):
        print("\n\n\n\n----------------------------------------------------------------\n----------------------------------------------------------------\nINTERNET FAIL!!!!!!!\n----------------------------------------------------------------\n----------------------------------------------------------------\n")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text=f"Sorry, an error occurred: '{str(context.error)}'.\n\nIf it's something strange please contact @igor_ivanter for questions.\n\nType: {type(context.error)}.\n\nTrying to print: {context.error}")


def help_command(update, context):
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


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add the command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('error', error))
    dispatcher.add_handler(CommandHandler('timeout', timeout_error))

    # add the text message hadler
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), text_message))

    # add the voice note handler
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_message))

    # add the error handler to dispatcher
    dispatcher.add_error_handler(error_handler)

    # add the callbackquery handler - this function defines what happenes when one of the inline buttons gets pressed
    dispatcher.add_handler(CallbackQueryHandler(button_click_handler))

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
