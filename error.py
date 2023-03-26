from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import openai


def handle_error(update, context):
    inline_keyboard = [[InlineKeyboardButton('Retry', callback_data='retry')]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    if isinstance(context.error, openai.error.Timeout):
        error_message = context.bot.send_message(
            chat_id=update.effective_chat.id, text="Hey there, I'm sorry, but I couldn't get you an answer in reasonable time.\n\nThis might be because too many users are trying to get a response.\n\nYou can repeat your request and I will do my best to get you an answer this time 😎.\n\nYour chat history isn't affected by this error.", reply_markup=reply_markup)
        context.user_data["last_error_message"] = error_message
    elif isinstance(context.error, telegram.error.NetworkError):
        print("\n\n\n\n----------------------------------------------------------------\n----------------------------------------------------------------\nINTERNET FAIL!!!!!!!\n----------------------------------------------------------------\n----------------------------------------------------------------\n")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Sorry, an error occurred: '{str(context.error)}'.\n\nIf it's something strange please contact @igor_ivanter for questions.\n\nType: {type(context.error)}.\n\nTrying to print: {context.error}")