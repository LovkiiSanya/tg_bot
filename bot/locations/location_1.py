from bot.enemies import Goblin, Wolf, Orc, Golem, Dragon
from django.db.models import F
from bot.models import Character
from django.core.management.base import BaseCommand
from bot.enemies import Enemy
import telebot
import schedule
import time
import os
import telebot

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

goblin1 = Goblin.objects.create(name='Goblin1', level=1)
goblin2 = Goblin.objects.create(name='Goblin2', level=1)
goblin3 = Goblin.objects.create(name='Goblin3', level=1)


@bot.message_handler(commands=['location_1'])
def start_battle(message):
    user_id = message.from_user.id
    user = Character.objects.get(user_id=user_id)
    print(f"User {user.nickname} is starting location 1 battle.")


def character_attack(character, enemy):
    # Логика атаки персонажа
    pass


def enemy_attack(character, enemy):
    # Логика атаки противника
    pass


# def run_battle(character, enemy):
#     character_attack(character, enemy)
#     time.sleep(1)  # Пауза между ходами
#     enemy_attack(character, enemy)
#
#     user = Character.objects.get(user_id=message.from_user.id)
#     goblin_instances = Goblin.objects.filter(level=1)


bot.polling(none_stop=True)
