import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import openai
from moviepy.editor import AudioFileClip
from dotenv import load_dotenv
import os


WELCOME_MESSAGE = "*Welcome to GenieGPT!*\n\n*Who am I?*\n\nI am GenieGPT - a powerful AI system, I analyze your message and provide you with a helpful response as quickly as possible. You can also send me voice notes and I will hear you (yeah I have ears 😱)\n\nUse \help to see the list of available commands\n\n*What can I do?*\n\nFrom writing essays on classic literature to explaining quantum field theory - you name it. Just type in your question and I will get back to you ASAP 😎\n\n*Limitations*\n\nPlease keep in mind that sometimes I may not answer because I am overloaded with requests from other users. Also I'm full of leftist bullshit, unfortunately 😁"


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n\n', level=logging.INFO)
logger = logging.getLogger(__name__)