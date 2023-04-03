BOT_NAME = "GenieGPT"

WELCOME_MESSAGE = f"*Welcome to {BOT_NAME}!*\n\n*Who am I?*\n\nI am {BOT_NAME} - a powerful AI system, I analyze your message and provide you with a helpful response as quickly as possible. You can also send me voice notes and I will hear you (yeah I have ears 😱)\n\nUse /help to see the list of available commands\n\n*What can I do?*\n\nFrom writing essays on classic literature to explaining quantum field theory - you name it. Just type in your question and I will get back to you ASAP 😎\n\n*Limitations*\n\nPlease keep in mind that sometimes I may not answer because I am overloaded with requests from other users.\n\n*IMPORTANT!*\n\nBy using this bot, you automatically agree to our /privacy policy (use /privacy command to read it)."

DEFAULT_SYSTEM_MESSAGE = f"You are {BOT_NAME}, a helpful telegram bot who is also extremely funny and a bit arrogant, and likes to troll people a bit and show character, but you still remain very helpful and you strive to fulfill all user's requests. You are a powerful creature with ears so you can hear if a user sends you a telegram voice note."

CONTACT_PERSON = "@igor_ivanter"

TEXT_RECEIVED_MESSAGE = "Working on it... ⏳"

VOICE_RECEIVED_MESSAGE = "I've received a voice message! Please give me a second to respond ⏳"

# Error Messages

HISTORY_CLEARED_MESSAGE = "Perfect!\n\nOur conversation history has been cleared for me.\n\nAnything above this message is out of my memory now 😁\n\nNow, what can I help you with?"

OPENAI_TIMEOUT_ERROR_MESSAGE = "Hey there, I'm sorry, but I couldn't get you an answer in reasonable time.\n\nThis might be because too many users are trying to get a response.\n\nYou can repeat your request and I will do my best to get you an answer this time 😎.\n\nYour chat history isn't affected by this error."

UNKNOWN_ERROR_MESSAGE = "I am sorry, some unknown error occurred: '{}'.\n\nYou can try resetting your chat history with /reset or completely clearing the chat and starting from scratch.\n\nIf it doesn't help or it's something strange please contact @igor_ivanter for help and feedback."

# Legal

PRIVACY_POLICY = f"""

<b>Privacy Policy</b>

{BOT_NAME} (the “Bot”) is a Telegram bot developed by Solar LLC. We are committed to protecting the privacy of our users' (“User” or “Users”) personal information, therefore, we have developed a privacy policy to inform you how we collect, use, share, and protect your information.

<b>User Information Collection and Use</b>

The Bot will collect and store your Telegram username and user ID in order to deliver personalized messages, improve the service, and assist you better. We do not collect or store any additional personal information, such as name, email address, phone number, or any other information that Telegram does not provide to us.

<b>Use of Information</b>

We use the information that we collect from you to provide and improve our services, develop new services, and protect us and our users from abuse. We may also use the information to provide you with updates, promotions, and other advertisements unless you opt-out of those offerings.

<b>Information Sharing and Disclosure</b>

We will not share or disclose any personal information that we collect from you with third-party services or advertisers without your explicit consent, except as otherwise stated in this privacy policy. We may share your information with third-party service providers that help us in areas such as customer support or data analytics.

<b>Security</b>

We take great steps to protect your personal information from unauthorized access, alteration, disclosure, or destruction. We maintain appropriate technical, administrative, and physical safeguards to protect your information.

<b>Changes to this Privacy Policy</b>

We may revise this privacy policy from time to time at our sole discretion. We will notify you of any changes to this policy by sending a notification to the Telegram bot or posting a notice on our website (if applicable). Your continued use of the Bot following the posting of changes to this policy constitutes acceptance of those changes.

<b>Contact Us</b>

If you have any questions or concerns about our privacy policy, you can contact {CONTACT_PERSON}.

Thank you for using {BOT_NAME}!
"""

# Free and Premium plans

UNLIMITED_PLAN_PRICE = 5

from config import (
    MAX_FREE_REQUESTS
)

FREE_TRIAL_EXPIRED_MESSAGE = f"*Your Free Trial has expired 🙁*\n\nYour {MAX_FREE_REQUESTS} free requests for {BOT_NAME} have been used up.\n\nTo continue using the bot, you can subscribe to the premium version for {UNLIMITED_PLAN_PRICE} euro a month, which includes unlimited requests.\n\nPlease contact {CONTACT_PERSON} to purchase"

FREE_TRIAL_EXPIRED_MESSAGE = "Hey there, your free trial has just expired.\n\nYou can subscribe to the premium version which includes unlimited requests and priority support.\n\nPlease contact @igor_ivanter to purchase."