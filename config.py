import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n', level=logging.DEBUG)
logger = logging.getLogger(__name__)

VOICE_MESSAGE_FILE_PATH_BASE = "audio/voice_message"
VOICE_MESSAGE_MP3 = VOICE_MESSAGE_FILE_PATH_BASE + ".mp3"
VOICE_MESSAGE_OGG = VOICE_MESSAGE_FILE_PATH_BASE + ".ogg"

USER_DATA_FILE_PATH = "./users/user_data.json"