import telegram
from handlers import handle_message_text


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
