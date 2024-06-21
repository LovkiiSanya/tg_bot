# import os
# import telebot
# from django.conf import settings
# from .models import Character
#
# TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# bot = telebot.TeleBot(TOKEN)
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     user, created = Character.objects.get_or_create(user_id=message.from_user.id)
#     if created:
#         user.hp = 100
#         user.mp = 50
#         user.cp = 10
#         user.save()
#
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#         tank_button = telebot.types.KeyboardButton('Tank')
#         duelist_button = telebot.types.KeyboardButton('Duelist')
#         mage_button = telebot.types.KeyboardButton('Mage')
#         markup.row(tank_button, duelist_button, mage_button)
#
#         bot.reply_to(message, "Welcome to the game! Your character has been created. Choose your class:",
#                      reply_markup=markup)
#     else:
#         bot.reply_to(message, "Welcome back!")
#
#
# @bot.message_handler(func=lambda message: True)
# def handle_class_choice(message):
#     if message.text in ['Tank', 'Duelist', 'Mage']:
#         user = Character.objects.get(user_id=message.from_user.id)
#         user.nickname = message.text
#
#         if message.text == 'Tank':
#             user.hp += 50
#             user.cp -= 5
#             user.mp -= 10
#         elif message.text == 'Duelist':
#             user.cp += 20
#             user.hp -= 20
#             user.mp -= 10
#         elif message.text == 'Mage':
#             user.mp += 30
#             user.hp -= 30
#             user.cp -= 5
#
#         user.save()
#         bot.reply_to(message, f"You are now a {message.text}! Enjoy your adventure.")
#     else:
#         bot.reply_to(message, "Please choose a valid class.")
