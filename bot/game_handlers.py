import logging
import telebot


def start(bot, message):
    welcome_text = (
        "Welcome! I'm your friendly bot. Please use the following commands to interact with me:\n"
        "/start - Start the bot and see this message\n"
        "/sendphoto - Send a photo\n"
        "/commands - List all commands"
    )
    bot.send_message(message.chat.id, welcome_text)
    logging.info(f"Sent start message to user {message.chat.id}.")


def echo(bot, message):
    bot.send_message(message.chat.id, message.text)
    logging.info(f"Echoed message to user {message.chat.id}: {message.text}")


def unknown(bot, message):
    bot.send_message(message.chat.id, "Sorry, I didn't understand that command.")
    logging.info(f"Sent unknown command message to user {message.chat.id}.")


def send_photo(bot, message):
    photo_path = '/home/sanya/Загрузки/dc7dfea46ea3d058bc9cc69bfdef58ee.jpg'
    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file,caption='это вы?')
            logging.info(f"Sent photo to user {message.chat.id}.")
    except Exception as e:
        bot.send_message(message.chat.id, "Failed to send photo.")
        logging.error(f"Failed to send photo to user {message.chat.id}: {e}")


def list_commands(bot, message):
    commands = [
        "/start - Start the bot and see the welcome message",
        "/sendphoto - Send a photo",
        "/commands - List all commands"
    ]
    commands_text = "\n".join(commands)
    bot.send_message(message.chat.id, f"Available commands:\n{commands_text}")
    logging.info(f"Sent command list to user {message.chat.id}.")
