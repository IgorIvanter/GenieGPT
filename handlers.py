import openai
import telegram
import config
from moviepy.editor import AudioFileClip
from messages import DEFAULT_SYSTEM_MESSAGE


logging = config.logging


OPENAI_REQUEST_TIMEOUT = 60  # openai request timeout in seconds


def handle_message_text(update, context):
    logging.debug("Entering handle_message_text")
    context.user_data['last_request'] = update.message.text
    context.user_data['last_update'] = update
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
    logging.debug("Exiting handle_message_text")


def handle_message_voice(update, context):
    logging.debug("Entering handle_message_voice")
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
    handle_message_text(update, context)
    logging.debug("Exiting handle_message_voice")
