import os
import telebot
from django.core.management.base import BaseCommand
from bot.models import Character
from bot.enemies import Enemy, Goblin, Wolf, Orc, Golem, Dragon

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


def clear_and_create_enemies():
    Enemy.objects.all().delete()

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

    enemies = goblins + wolves + orcs + golems + dragons

    for enemy in enemies:
        enemy.save()


clear_and_create_enemies()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            user, created = Character.objects.get_or_create(user_id=message.from_user.id)
            if created:
                bot.reply_to(message, "Welcome to the game! Please enter your character's name:")
                bot.register_next_step_handler(message, set_nickname)
            else:
                bot.reply_to(message, "Welcome back!")

        def set_nickname(message):
            nickname = message.text
            user = Character.objects.get(user_id=message.from_user.id)
            user.nickname = nickname
            user.save()

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            tank_button = telebot.types.KeyboardButton('Tank')
            duelist_button = telebot.types.KeyboardButton('Duelist')
            mage_button = telebot.types.KeyboardButton('Mage')
            markup.row(tank_button, duelist_button, mage_button)

            bot.reply_to(message, "Great! Now choose your class:", reply_markup=markup)
            bot.clear_step_handler(message)
            bot.register_next_step_handler(message, set_class)

        def set_class_selection(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            tank_button = telebot.types.KeyboardButton('Tank')
            duelist_button = telebot.types.KeyboardButton('Duelist')
            mage_button = telebot.types.KeyboardButton('Mage')
            markup.row(tank_button, duelist_button, mage_button)

            bot.send_message(message.chat.id, "Choose your class:", reply_markup=markup)
            bot.clear_step_handler(message)
            bot.register_next_step_handler(message, set_class)

        def set_class(message):
            user = Character.objects.get(user_id=message.from_user.id)
            role = message.text

            class_descriptions = {
                'Mage': "The mage has high one-time damage, but a small supply of life and armor.",
                'Tank': "Tank - everything is clear from the name! Lots of life and armor, low damage.",
                'Duelist': "Duelist - a born killer, average characteristics but good chances for crit and dodge."
            }

            if role in class_descriptions:
                user.role = role

                if role == 'Tank':
                    user.hp += 100
                    user.cp += 40
                    user.mp += 10
                    user.dmg += 50
                elif role == 'Duelist':
                    user.cp += 50
                    user.hp += 50
                    user.mp += 10
                    user.dmg += 75
                elif role == 'Mage':
                    user.mp += 20
                    user.hp += 25
                    user.cp += 25
                    user.dmg += 90

                user.save()

                description = class_descriptions[role]
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                confirm_button = telebot.types.KeyboardButton('Confirm')
                back_button = telebot.types.KeyboardButton('Back to class selection')
                markup.row(confirm_button, back_button)

                bot.reply_to(message, f"{description} Choose your action:", reply_markup=markup)
                bot.clear_step_handler(message)
                bot.register_next_step_handler(message, handle_class_confirmation)
            else:
                bot.reply_to(message, "Please choose a valid class.")
                bot.clear_step_handler(message)
                bot.register_next_step_handler(message, set_class)

        def handle_class_confirmation(message):
            user = Character.objects.get(user_id=message.from_user.id)
            action = message.text

            if action == 'Confirm':
                bot.reply_to(message, f"You confirmed your class {user.role}. Enjoy your adventure!\n"
                                      f"Use /stat to see you character stats")
            elif action == 'Back to class selection':
                set_class_selection(message)
            else:
                bot.reply_to(message, "Please choose a valid action.")
                bot.clear_step_handler(message)
                bot.register_next_step_handler(message, handle_class_confirmation)

        @bot.message_handler(commands=['stat'])
        def show_stats(message):
            user = Character.objects.get(user_id=message.from_user.id)
            stats_message = (
                f"Character Stats:\n"
                f"Nickname: {user.nickname}\n"
                f"Role: {user.role}\n"
                f"HP: {user.hp}\n"
                f"MP: {user.mp}\n"
                f"CP: {user.cp}\n"
                f"Damage: {user.dmg}\n"
                f"Experience: {user.exp}\n"
                f"Level: {user.level}\n"
                f"Dodge: {user.dodge:.2f}%\n"
                f"Crit: {user.crit:.2f}\n"
                f"Crit Chance: {user.crit_chance:.2f}%"
            )
            bot.reply_to(message, stats_message)

        @bot.message_handler(commands=['roll'])
        def roll_dice(message):
            try:
                user = Character.objects.get(user_id=message.from_user.id)
                user.apply_random_effect()
                bot.reply_to(message, f"Effect applied: {user.effects}")
            except Character.DoesNotExist:
                bot.reply_to(message, "You don't have a character yet. Use /start to create one.")

        @bot.message_handler(commands=['enemies'])
        def show_enemies(message):
            enemies = Enemy.objects.all()
            if enemies.exists():
                response = "List of enemies:\n"
                for enemy in enemies:
                    response += f"{enemy.enemy_type} - {enemy.name}, HP: {enemy.get_hp()}, DMG: {enemy.get_dmg()}, CP: {enemy.get_cp()}, Level: {enemy.level}\n"
            else:
                response = "No enemies."

            bot.send_message(message.chat.id, response)

        bot.polling(none_stop=True)
