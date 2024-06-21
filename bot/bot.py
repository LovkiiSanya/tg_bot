import telebot
import logging
from game_handlers import start, echo, unknown, send_photo, list_commands

API_TOKEN = '5077449658:AAHSF7olQifxn75ao5-kZJ4q3iB4S4BwOFg'
bot = telebot.TeleBot(API_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Команда /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.info(f"User {message.chat.id} started the bot.")
    start(bot, message)


# Команда /sendphoto
@bot.message_handler(commands=['sendphoto'])
def handle_send_photo(message):
    logging.info(f"User {message.chat.id} requested to send a photo.")
    send_photo(bot, message)


# Команда /commands
@bot.message_handler(commands=['commands'])
def handle_commands(message):
    logging.info(f"User {message.chat.id} requested the list of commands.")
    list_commands(bot, message)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    logging.info(f"User {message.chat.id} sent a message: {message.text}")
    echo(bot, message)


# Обработчик неизвестных команд
@bot.message_handler(func=lambda message: message.text.startswith('/'))
def handle_unknown_command(message):
    logging.info(f"User {message.chat.id} sent an unknown command: {message.text}")
    unknown(bot, message)


if __name__ == '__main__':
    logging.info("Starting bot.")
    bot.polling()
