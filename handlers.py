import openai
import telegram
import config
from moviepy.editor import AudioFileClip

from messages import (
    DEFAULT_SYSTEM_MESSAGE,
    TEXT_RECEIVED_MESSAGE,
    VOICE_RECEIVED_MESSAGE
)


logging = config.logging

OPENAI_REQUEST_TIMEOUT = 60  # openai request timeout in seconds


def handle_message_text(update, context):
    logging.debug("Entering handle_message_text")

    # Store last update and last message for the case of error
    context.user_data['last_request'] = update.message.text
    context.user_data['last_update'] = update

    # Check if the chat history hasn't been recorded yet or if recorded improperly
    if context.user_data.get('messages') == None:
        context.user_data["messages"] = [{
            "role": "system",
            "content": DEFAULT_SYSTEM_MESSAGE
        }]
    elif context.user_data["messages"][0]["role"] != "system":
        raise NameError(
            "First message role is not system, but '{}'".format(
            context.user_data["messages"][0]["role"]
            )
        )
    
    # Add the latest user message to history
    context.user_data["messages"].append({
        "role": "user",
        "content": update.message.text
    })
    # Send a 'text received' message
    chat_message = update.message.reply_text(
        text=TEXT_RECEIVED_MESSAGE
    )
    # Send typing action
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=telegram.ChatAction.TYPING
    )
    # Get a response from GPT-3.5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context.user_data["messages"],
        request_timeout=OPENAI_REQUEST_TIMEOUT
    )
    # Extract text from response
    response_text = response["choices"][0]["message"]["content"]
    context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=chat_message.message_id
    )
    # Send the response text into the chat
    update.message.reply_text(
        text=f"*[Bot]:* {response_text}",
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    # Add response text to chat history
    context.user_data["messages"].append(
        {"role": "assistant", "content": response_text})
    # Shorten chat history to no more then 10 last messages (avoid overflow)
    context.user_data["messages"] = context.user_data["messages"][-10:]
    context.user_data["messages"][0] = {
        "role": "system",
        "content": DEFAULT_SYSTEM_MESSAGE
    }
    logging.debug("Exiting handle_message_text")


def handle_message_voice(update, context):
    logging.debug("Entering handle_message_voice")
    # Send a 'voice received' message
    voice_received_message = update.message.reply_text(
        VOICE_RECEIVED_MESSAGE
    )
    # Download the voice note and convert to mp3
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download("voice_message.ogg")
    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")
    audio_file = open("voice_message.mp3", "rb")
    # Get the transcription from Whisper API
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    update.message.text = transcript
    # Delete the 'voice received' message
    context.bot.delete_message(
        chat_id=update.message.chat_id,
        message_id=voice_received_message.message_id
    )
    # Send transcript to user
    update.message.reply_text(
        text=f"*[You]:* _{transcript}_",
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    handle_message_text(update, context)
    logging.debug("Exiting handle_message_voice")
