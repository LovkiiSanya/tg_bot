import os
import telebot
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from bot.models import Character
from bot.enemies import Enemy, Goblin, Wolf, Orc, Golem, Dragon
from bot.locations.location_1 import battle
from django.db import transaction, IntegrityError
import re

ALLOWED_CHARACTERS_PATTERN = re.compile(r'^[0-9a-zA-Zа-яёєіїА-ЯЁЄІЇ]+$')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


def create_character_if_not_exists(user_id):
    try:
        with transaction.atomic():
            # Проверяем, существует ли уже персонаж с данным user_id
            character = Character.objects.select_for_update().get(user_id=user_id)
            return character, False
    except Character.DoesNotExist:
        # Если не существует, создаем нового персонажа
        character = Character(
            user_id=user_id,
            nickname='default_nickname',
            role='default_role',
            hp=100,
            mp=10,
            cp=10,
            dmg=10,
            exp=0,
            level=1,
            state='awaiting_nickname'
        )
        character.save()
        return character, True


def clear_and_create_enemies():
    Enemy.objects.all().delete()

    enemies = []

    goblins = [
        Goblin(name="Goblin", level=1),
        Goblin(name="Goblin Fighter", level=2),
        Goblin(name="Goblin Champion", level=3)
    ]

    wolves = [
        Wolf(name="Wolf Pup", level=1),
        Wolf(name="Wolf", level=2),
        Wolf(name="Alpha Wolf", level=3)
    ]

    orcs = [
        Orc(name="Orc Warrior", level=1),
        Orc(name="Orc Berserker", level=2),
        Orc(name="Orc Warlord", level=3)
    ]

    golems = [
        Golem(name="Stone Golem", level=1),
        Golem(name="Iron Golem", level=2),
        Golem(name="Diamond Golem", level=3)
    ]

    dragons = [
        Dragon(name="Lil Dragon", level=1),
        Dragon(name="Fire Dragon", level=2),
        Dragon(name="King Dragon", level=3)
    ]

    enemies.extend(goblins + wolves + orcs + golems + dragons)

    for enemy in enemies:
        enemy.save()


clear_and_create_enemies()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def get_or_none(model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def handle(self, *args, **options):

        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            user_id = message.from_user.id
            try:
                character, created = create_character_if_not_exists(user_id)
                if created:
                    bot.reply_to(message, "Welcome to the game! Please enter your character's name:")
                else:
                    bot.reply_to(message, "Welcome back!")
            except IntegrityError:
                bot.reply_to(message, "There was an error creating your character. Please try again.")

        # @bot.message_handler(func=lambda message: True)
        # def handle_all_messages(message):
        #     if message.text.startswith('/start'):
        #         self.send_welcome(message)
        #     else:
        #         bot.reply_to(message, "Please start the game with /start command.")

        def get_or_none(model, **kwargs):
            try:
                return model.objects.get(**kwargs)
            except model.DoesNotExist:
                return None

        @bot.message_handler(
            func=lambda message: get_or_none(Character, user_id=message.from_user.id) and
                                 get_or_none(Character, user_id=message.from_user.id).state == 'awaiting_nickname'
        )
        def set_nickname(message):
            user = get_or_none(Character, user_id=message.from_user.id)
            if user:
                nickname = message.text.strip()  # Удаляем лишние пробелы в начале и конце
                if re.match(ALLOWED_CHARACTERS_PATTERN, nickname) and len(nickname) <= 20:
                    user.nickname = nickname
                    user.state = 'class_selection'
                    user.save()

                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    tank_button = telebot.types.KeyboardButton('Tank')
                    duelist_button = telebot.types.KeyboardButton('Duelist')
                    mage_button = telebot.types.KeyboardButton('Mage')
                    markup.row(tank_button, duelist_button, mage_button)

                    bot.reply_to(message, "Great! Now choose your class:", reply_markup=markup)
                else:
                    bot.reply_to(message,
                                 "Invalid characters in nickname. Please use only numbers and letters in Russian, "
                                 "Ukrainian, or English.(20 symbols)")
            else:
                bot.reply_to(message, "Character not found. Please start a new game with /start.")

        @bot.message_handler(
            func=lambda message: Command.get_or_none(Character, user_id=message.from_user.id) and Command.get_or_none(
                Character, user_id=message.from_user.id).state == 'class_selection'
        )
        def set_class(message):
            user = Command.get_or_none(Character, user_id=message.from_user.id)
            if user:
                role = message.text

                class_descriptions = {
                    'Mage': "The mage has high one-time damage, but a small supply of life and armor.",
                    'Tank': "Tank - everything is clear from the name! Lots of life and armor, low damage.",
                    'Duelist': "Duelist - a born killer, average characteristics but good chances for crit and dodge."
                }

                if role in class_descriptions:
                    temp_stats = {
                        'hp': user.hp,
                        'cp': user.cp,
                        'mp': user.mp,
                        'dmg': user.dmg
                    }

                    if role == 'Tank':
                        temp_stats['hp'] += 100
                        temp_stats['cp'] += 40
                        temp_stats['mp'] += 10
                        temp_stats['dmg'] += 50
                    elif role == 'Duelist':
                        temp_stats['cp'] += 50
                        temp_stats['hp'] += 50
                        temp_stats['mp'] += 10
                        temp_stats['dmg'] += 75
                    elif role == 'Mage':
                        temp_stats['mp'] += 20
                        temp_stats['hp'] += 25
                        temp_stats['cp'] += 25
                        temp_stats['dmg'] += 90

                    user.temp_stats = temp_stats
                    user.role = role
                    user.state = 'class_confirmation'
                    user.save()

                    description = class_descriptions[role]
                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    confirm_button = telebot.types.KeyboardButton('Confirm')
                    back_button = telebot.types.KeyboardButton('Back to class selection')
                    markup.row(confirm_button, back_button)

                    bot.reply_to(message, f"{description} Choose your action:", reply_markup=markup)
                else:
                    bot.reply_to(message, "Please choose a valid class.")
                    bot.clear_step_handler(message)
                    bot.register_next_step_handler(message, set_class)
            else:
                bot.reply_to(message, "Character not found. Please start a new game with /start.")

        @bot.message_handler(
            func=lambda message: Command.get_or_none(Character, user_id=message.from_user.id) and Command.get_or_none(
                Character, user_id=message.from_user.id).state == 'class_confirmation'
        )
        def handle_class_confirmation(message):
            user = Command.get_or_none(Character, user_id=message.from_user.id)
            if user:
                action = message.text

                if action == 'Confirm':
                    user.hp = user.temp_stats['hp']
                    user.cp = user.temp_stats['cp']
                    user.mp = user.temp_stats['mp']
                    user.dmg = user.temp_stats['dmg']
                    user.state = 'location_1'
                    user.save()

                    markup = telebot.types.ReplyKeyboardRemove()  # Удалить кнопки
                    bot.send_message(message.chat.id,
                                     f"You confirmed your class {user.role}. Enjoy your adventure!\nUse /stat to see your "
                                     f"character stats",
                                     reply_markup=markup)

                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    location_1_button = telebot.types.KeyboardButton('/location_1')
                    markup.add(location_1_button)
                    bot.send_message(message.chat.id, "Choose your location:", reply_markup=markup)

                elif action == 'Back to class selection':
                    user.state = 'class_selection'
                    user.save()
                    set_class_selection(message)
                else:
                    bot.reply_to(message, "Please choose a valid action.")
                    bot.clear_step_handler(message)
                    bot.register_next_step_handler(message, handle_class_confirmation)
            else:
                bot.reply_to(message, "Character not found. Please start a new game with /start.")

        def set_class_selection(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            tank_button = telebot.types.KeyboardButton('Tank')
            duelist_button = telebot.types.KeyboardButton('Duelist')
            mage_button = telebot.types.KeyboardButton('Mage')
            markup.row(tank_button, duelist_button, mage_button)

            bot.send_message(message.chat.id, "Choose your class:", reply_markup=markup)

        @bot.message_handler(commands=['location_1'])
        def handle_location_1(message):
            user = Character.objects.get(user_id=message.from_user.id)
            if user.state != 'location_1':
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            try:
                character = Character.objects.get(user_id=message.from_user.id)
                enemies = [
                    Goblin(name="Goblin", level=1),
                    Goblin(name="Goblin", level=1),
                    Goblin(name="Goblin Fighter", level=2),
                    Dragon(name="King Dragon", level=3)
                ]
                battle(bot, message.chat.id, character, enemies)
            except Character.DoesNotExist:
                bot.send_message(message.chat.id, "Character not found,create new character /start")

        @bot.message_handler(commands=['stat'])
        def show_stats(message):
            user = Character.objects.get(user_id=message.from_user.id)
            exp_to_next_level = 100 * user.level
            stats_message = (
                f"Character Stats:\n"
                f"Nickname: {user.nickname}\n"
                f"Role: {user.role}\n"
                f"HP: {user.hp}\n"
                f"MP: {user.mp}\n"
                f"CP: {user.cp}\n"
                f"Damage: {user.dmg}\n"
                f"Experience: {user.exp}/{exp_to_next_level}\n"
                f"Level: {user.level}\n"
                f"Dodge: {user.dodge:.2f}%\n"
                f"Crit: {user.crit:.2f}\n"
                f"Crit Chance: {user.crit_chance:.2f}%"
            )
            bot.reply_to(message, stats_message)

        bot.polling(none_stop=True)
