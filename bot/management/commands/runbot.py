import os
import telebot
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from bot.models import Character
from bot.enemies import Enemy, Goblin, Wolf, Orc, Golem, Dragon, Skeleton, Cerberus, BossFairy, Shadow, Cobalt, \
    BossBear,BossPhoenix,Hydra
from bot.locations.location_1 import battle
from django.db import transaction, IntegrityError
import re
from functools import wraps

ALLOWED_CHARACTERS_PATTERN = re.compile(r'^[0-9a-zA-Zа-яёєіїА-ЯЁЄІЇ]+$')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


def requires_character(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        if not Character.objects.filter(user_id=user_id).exists():
            bot.reply_to(message, "Please start the game with /start command.")
            return
        return func(message, *args, **kwargs)

    return wrapper


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

    hydras = [
        Hydra(name="Hydra", level=1),
        Hydra(name="Poisonous Hydra", level=2),
        Hydra(name="Ignis Hydra", level=3)
    ]
    shadows = [
        Shadow(name="Shadow", level=1),
        Shadow(name="Shadow assassin", level=2),
        Shadow(name="Shadow Lord", level=3)
    ]

    skeletons = [
        Skeleton(name="Skeleton", level=1),
        Skeleton(name="Skeleton Knight", level=2),
        Skeleton(name="Skeleton Reaper", level=3)
    ]

    cobalts = [
        Cobalt(name="Cobalt", level=1),
        Cobalt(name="Cobalt Mutant", level=2),
        Cobalt(name="Cobalt Chief", level=3)
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

    cerbers = [
        Cerberus(name="Cerberus", level=1),
        Cerberus(name="Spirit Cerberus", level=2),
        Cerberus(name="Mythical Cerberus", level=3)
    ]

    boss_bear = [
        BossBear(name="Furious Bear", level=1, skills={"root": True})
    ]

    boss_fairy = [
        BossFairy(name="Ancient Fairy", level=1, skills={"rage": True})
    ]

    boss_phoenix = [
        BossFairy(name="Ancient Fairy", level=1, skills={"reincarnation": True})
    ]
    enemies.extend(goblins + wolves + orcs + golems + dragons + skeletons + shadows + cobalts + boss_bear + boss_fairy + boss_phoenix+cerbers)

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
                    user.state = 'location_selection'
                    user.save()

                    markup = telebot.types.ReplyKeyboardRemove()  # Удалить кнопки
                    bot.send_message(message.chat.id,
                                     f"You confirmed your class {user.role}. Enjoy your adventure!\nUse /stat to see "
                                     f"your character stats and /restart to restart :)",
                                     reply_markup=markup)

                    # Отправляем клавиатуру с выбором локации и кнопкой "Back"
                    show_location_selection(message)

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

        def show_location_selection(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            forest_button = telebot.types.KeyboardButton('Mistery Forest (Easy)')
            catacombs_button = telebot.types.KeyboardButton('Ancient Catacombs (Normal)')
            magma_button = telebot.types.KeyboardButton('Magma Fields (Hard)')
            dragons_button = telebot.types.KeyboardButton('Dragons Capital (Locked)')
            markup.add(forest_button, catacombs_button, magma_button, dragons_button)
            bot.send_message(message.chat.id, "Choose your location:", reply_markup=markup)

        def set_class_selection(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            tank_button = telebot.types.KeyboardButton('Tank')
            duelist_button = telebot.types.KeyboardButton('Duelist')
            mage_button = telebot.types.KeyboardButton('Mage')
            markup.row(tank_button, duelist_button, mage_button)

            bot.send_message(message.chat.id, "Choose your class:", reply_markup=markup)

        @bot.message_handler(func=lambda message: message.text == 'Back')
        def handle_back(message):
            user = Character.objects.get(user_id=message.from_user.id)
            user.state = 'location_selection'
            user.in_battle = False
            user.save()
            show_location_selection(message)

        @bot.message_handler(func=lambda message: message.text == 'Mistery Forest (Easy)')
        @requires_character
        def handle_forest(message):
            user = Character.objects.get(user_id=message.from_user.id)
            if user.state != 'location_selection':
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            current_level = user.current_forest_level  # Текущий уровень леса пользователя
            user.state = f'location_1_level_{current_level}'  # Устанавливаем начальное состояние
            user.save()

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(current_level, 11):
                markup.add(telebot.types.KeyboardButton(f'Mistery Forest Level {i}'))
            markup.add(telebot.types.KeyboardButton('Back'))  # Добавляем кнопку "Back"
            bot.send_message(message.chat.id, "Choose your level:", reply_markup=markup)

        @bot.message_handler(func=lambda message: message.text.startswith('Mistery Forest Level'))
        @requires_character
        def handle_forest_level(message):
            user = Character.objects.get(user_id=message.from_user.id)
            expected_state = f'location_1_level_{user.current_forest_level}'

            print(f"User state before handling forest level: {user.state}")  # Отладочное сообщение
            print(f"Expected state: {expected_state}")  # Отладочное сообщение

            if user.state != expected_state:
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            level = int(message.text.split()[-1])
            if level != user.current_forest_level:
                bot.reply_to(message, "You can only play the next available level.")
                return

            enemies = get_forest_level_enemies(level)
            if enemies:
                user.state = f'location_1_level_{level}'  # Устанавливаем новый state для текущего уровня
                user.in_battle = True

                print(f"User state after setting new level: {user.state}")  # Отладочное сообщение

                user.save()
                battle(bot, message.chat.id, user, enemies)
            else:
                bot.reply_to(message, "Invalid level.")

        def get_forest_level_enemies(level):
            if level == 1:
                return [Goblin(name="Goblin", level=1), Goblin(name="Goblin", level=1), Goblin(name="Goblin", level=1)]
            elif level == 2:
                return [Goblin(name="Goblin", level=1), Goblin(name="Goblin Fighter", level=2),
                        Goblin(name="Goblin", level=1)]
            elif level == 3:
                return [Goblin(name="Goblin", level=1), Goblin(name="Goblin Fighter", level=2),
                        Goblin(name="Goblin Champion", level=3)]
            elif level == 4:
                return [Wolf(name="Wolf Pup", level=1), Goblin(name="Goblin Fighter", level=2),
                        Goblin(name="Goblin Champion", level=3)]
            elif level == 5:
                return [Wolf(name="Wolf", level=2), Goblin(name="Goblin Fighter", level=2),
                        Goblin(name="Goblin Champion", level=3)]
            elif level == 6:
                return [Wolf(name="Alpha Wolf", level=3), Wolf(name="Wolf", level=2),
                        Goblin(name="Goblin Champion", level=3)]
            elif level == 7:
                return [Orc(name="Orc Warrior", level=1), Wolf(name="Wolf", level=2),
                        Goblin(name="Goblin Champion", level=3)]
            elif level == 8:
                return [Orc(name="Orc Warrior", level=1), Orc(name="Orc Berserker", level=2),
                        Wolf(name="Alpha Wolf", level=3)]
            elif level == 9:
                return [Orc(name="Orc Warrior", level=1), Orc(name="Orc Berserker", level=2),
                        Orc(name="Orc Warlord", level=3)]
            elif level == 10:
                return [BossFairy(name="Ancient Fairy", level=1, skills={"root": True})]
            return None

        @bot.message_handler(func=lambda message: message.text == 'Ancient Catacombs (Normal)')
        @requires_character
        def handle_catacombs(message):
            user = Character.objects.get(user_id=message.from_user.id)
            if user.state != 'location_selection':
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            current_level = user.current_catacombs_level  # Текущий уровень катакомб пользователя
            user.state = f'location_2_level_{current_level}'  # Устанавливаем начальное состояние
            user.save()

            print(f"User state after choosing Ancient Catacombs: {user.state}")  # Отладочное сообщение

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(current_level, 11):
                markup.add(telebot.types.KeyboardButton(f'Ancient Catacombs Level {i}'))
            markup.add(telebot.types.KeyboardButton('Back'))
            bot.send_message(message.chat.id, "Choose your level:", reply_markup=markup)

        @bot.message_handler(func=lambda message: message.text.startswith('Ancient Catacombs Level'))
        @requires_character
        def handle_catacombs_level(message):
            user = Character.objects.get(user_id=message.from_user.id)
            expected_state = f'location_2_level_{user.current_catacombs_level}'

            print(f"User state before handling Ancient Catacombs level: {user.state}")  # Отладочное сообщение
            print(f"Expected state: {expected_state}")  # Отладочное сообщение

            if user.state != expected_state:
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            level = int(message.text.split()[-1])
            if level != user.current_catacombs_level:
                bot.reply_to(message, "You can only play the next available level.")
                return

            enemies = get_catacombs_level_enemies(level)
            if enemies:
                user.state = f'location_2_level_{level}'  # Устанавливаем новый state для текущего уровня
                user.in_battle = True

                print(f"User state after setting new Ancient Catacombs level: {user.state}")  # Отладочное сообщение

                user.save()
                battle(bot, message.chat.id, user, enemies)
            else:
                bot.reply_to(message, "Invalid level.")

        def get_catacombs_level_enemies(level):
            if level == 1:
                return [Skeleton(name="Skeleton", level=1)]
            elif level == 2:
                return [Skeleton(name="Skeleton", level=1), Skeleton(name="Skeleton Knight", level=2)]
            elif level == 3:
                return [Skeleton(name="Skeleton Knight", level=2), Skeleton(name="Skeleton Reaper", level=3)]
            elif level == 4:
                return [Skeleton(name="Skeleton Reaper", level=3), Shadow(name="Shadow", level=1)]
            elif level == 5:
                return [Skeleton(name="Skeleton Reaper", level=3), Shadow(name="Shadow", level=1),
                        Shadow(name="Shadow Assassin", level=2)]
            elif level == 6:
                return [Shadow(name="Shadow", level=1), Shadow(name="Shadow Assassin", level=2),
                        Shadow(name="Shadow Lord", level=3)]
            elif level == 7:
                return [Shadow(name="Shadow Assassin", level=2), Shadow(name="Shadow Lord", level=3),
                        Cobalt(name="Cobalt", level=1)]
            elif level == 8:
                return [Shadow(name="Shadow Lord", level=3), Cobalt(name="Cobalt", level=1),
                        Cobalt(name="Cobalt Mutant", level=2)]
            elif level == 9:
                return [Cobalt(name="Cobalt", level=1), Cobalt(name="Cobalt Mutant", level=2),
                        Cobalt(name="Cobalt Chief", level=3)]
            elif level == 10:
                return [BossBear(name="Furious Bear", level=1,
                                 skills={"rage": True})]
            return None

        @bot.message_handler(func=lambda message: message.text == 'Magma Fields (Hard)')
        @requires_character
        def handle_magma(message):
            user = Character.objects.get(user_id=message.from_user.id)
            if user.state != 'location_selection':
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            current_level = user.current_magma_level  # Текущий уровень магмовых полей пользователя
            user.state = f'location_3_level_{current_level}'  # Устанавливаем начальное состояние
            user.save()

            print(f"User state after choosing Magma Fields: {user.state}")  # Отладочное сообщение

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(current_level, 11):
                markup.add(telebot.types.KeyboardButton(f'Magma Fields Level {i}'))
            markup.add(telebot.types.KeyboardButton('Back'))
            bot.send_message(message.chat.id, "Choose your level:", reply_markup=markup)

        @bot.message_handler(func=lambda message: message.text.startswith('Magma Fields Level'))
        @requires_character
        def handle_magma_level(message):
            user = Character.objects.get(user_id=message.from_user.id)
            expected_state = f'location_3_level_{user.current_magma_level}'

            print(f"User state before handling Magma Fields level: {user.state}")  # Отладочное сообщение
            print(f"Expected state: {expected_state}")  # Отладочное сообщение

            if user.state != expected_state:
                bot.reply_to(message, "You are not ready for this location yet.")
                return

            level = int(message.text.split()[-1])
            if level != user.current_magma_level:
                bot.reply_to(message, "You can only play the next available level.")
                return

            enemies = get_magma_level_enemies(level)
            if enemies:
                user.state = f'location_3_level_{level}'  # Устанавливаем новый state для текущего уровня
                user.in_battle = True

                print(f"User state after setting new Magma Fields level: {user.state}")  # Отладочное сообщение

                user.save()
                battle(bot, message.chat.id, user, enemies)
            else:
                bot.reply_to(message, "Invalid level.")

        def get_magma_level_enemies(level):
            if level == 1:
                return [Golem(name="Stone Golem", level=1)]
            elif level == 2:
                return [Golem(name="Stone Golem", level=1), Cerberus(name="Cerberus", level=2)]
            elif level == 3:
                return [Cerberus(name="Cerberus", level=2), Hydra(name="Hydra", level=3)]
            elif level == 4:
                return [Hydra(name="Hydra", level=3), Golem(name="Iron Golem", level=2)]
            elif level == 5:
                return [Golem(name="Iron Golem", level=2), Cerberus(name="Spirit Cerberus", level=2),
                        Hydra(name="Poisonous Hydra", level=2)]
            elif level == 6:
                return [Cerberus(name="Spirit Cerberus", level=2), Hydra(name="Poisonous Hydra", level=2),
                        Golem(name="Diamond Golem", level=3)]
            elif level == 7:
                return [Hydra(name="Ignis Hydra", level=3), Golem(name="Diamond Golem", level=3),
                        Cerberus(name="Mythical Cerberus", level=3)]
            elif level == 8:
                return [Golem(name="Stone Golem", level=1), Cerberus(name="Cerberus", level=2),
                        Hydra(name="Hydra", level=3)]
            elif level == 9:
                return [Cerberus(name="Spirit Cerberus", level=2), Hydra(name="Poisonous Hydra", level=2),
                        Golem(name="Diamond Golem", level=3)]
            elif level == 10:
                return [BossPhoenix(name="Phoenix", level=1,
                                    skills={"reincarnation": True})]  # Example boss name and skills, adjust as needed
            return None

        @bot.message_handler(commands=['stat'])
        @requires_character
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

        @bot.message_handler(commands=['restart'])
        def handle_restart(message):
            user_id = message.from_user.id
            bot.reply_to(message,
                         "Are you sure you want to restart your progress? This action cannot be undone. Reply with "
                         "'yes' or 'no'.")

        @bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'])
        def handle_confirmation(message):
            if message.text.lower() == 'yes':
                try:
                    character = Character.objects.get(user_id=message.from_user.id)

                    character.delete()
                    bot.send_message(message.chat.id, "Your progress has been reset. You can now start anew./start")
                except Character.DoesNotExist:
                    bot.send_message(message.chat.id,
                                     "No character found to reset. You might need to create a new character.")
            elif message.text.lower() == 'no':
                bot.send_message(message.chat.id, "Restart cancelled.")

        bot.polling(none_stop=True)
