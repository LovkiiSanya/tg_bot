import time
import random
from bot.management.commands.game_dice import apply_random_effect
from bot.models import Character
from bot.enemies import Goblin
import math


def reset_effects(character, original_methods):
    # Сброс эффектов
    if character.effects == "Double Damage":
        character.dmg /= 2
    elif character.effects == "Weaken opponents (-10% attack)":
        pass  # Реализуйте логику отмены ослабления противников
    elif character.effects == "Increase health by 20%":
        character.hp /= 1.2
    elif character.effects == "Disable dodge":
        character.calculate_dodge = original_methods['calculate_dodge']  # Вернуть исходный метод
    elif character.effects == "Damage reduction by 10%":
        character.dmg /= 0.9

    character.effects = ''
    character.save()


def battle(bot, chat_id, character, enemies):
    # Сохраняем оригинальные методы
    original_methods = {
        'calculate_dodge': character.calculate_dodge,
    }

    # Применяем случайный эффект перед началом боя
    apply_random_effect(character)
    bot.send_message(chat_id, f"🎲 Random effect applied: {character.effects}")
    time.sleep(1)

    character_hp = character.hp
    character_cp = character.cp
    battle_log = f"⚔️ The battle between {character.nickname} and a group of enemies has begun! ⚔️\n"
    bot.send_message(chat_id, battle_log)
    time.sleep(1)

    total_exp = 0
    battle_won = False

    for enemy in enemies:
        enemy_hp = enemy.get_hp()
        enemy_cp = enemy.get_cp()
        total_exp += enemy.exp_reward

        while character_hp > 0 and (enemy_hp > 0 or enemy_cp > 0):
            # Character attacks enemy
            if random.random() < (character.calculate_crit_chance() / 100):
                crit_dmg = character.calculate_crit()
                if enemy_cp > 0:
                    damage_to_enemy_cp = math.ceil(min(crit_dmg, enemy_cp))
                    enemy_cp -= damage_to_enemy_cp
                    battle_log = f"💥 Critical Hit! {character.nickname} attacks {enemy.name} and deals {damage_to_enemy_cp} CP damage. {enemy.enemy_type} has {enemy_cp} CP left.\n"
                else:
                    damage_to_enemy_hp = math.ceil(min(crit_dmg, enemy_hp))
                    enemy_hp -= damage_to_enemy_hp
                    battle_log = f"💥 Critical Hit! {character.nickname} attacks {enemy.name} and deals {damage_to_enemy_hp} HP damage. {enemy.enemy_type} has {enemy_hp} HP left.\n"
            else:
                if enemy_cp > 0:
                    damage_to_enemy_cp = math.ceil(min(character.dmg, enemy_cp))
                    enemy_cp -= damage_to_enemy_cp
                    battle_log = f"⚔️ {character.nickname} attacks {enemy.name} and deals {damage_to_enemy_cp} CP damage. {enemy.enemy_type} has {enemy_cp} CP left.\n"
                else:
                    damage_to_enemy_hp = math.ceil(min(character.dmg, enemy_hp))
                    enemy_hp -= damage_to_enemy_hp
                    battle_log = f"⚔️ {character.nickname} attacks {enemy.name} and deals {damage_to_enemy_hp} HP damage. {enemy.enemy_type} has {enemy_hp} HP left.\n"

            bot.send_message(chat_id, battle_log)
            time.sleep(1)

            if enemy_hp == 0 and enemy_cp == 0:
                battle_log = f"☠️ {enemy.name} has been defeated!\n"
                bot.send_message(chat_id, battle_log)
                time.sleep(1)
                break

            # Enemy attacks character
            if random.random() < (character.calculate_dodge() / 100):
                battle_log = f"🛡️ {character.nickname} dodges the attack from {enemy.name}!\n"
            else:
                if character_cp > 0:
                    damage_to_character_cp = math.floor(min(enemy.get_dmg(), character_cp))
                    character_cp -= damage_to_character_cp
                    battle_log = f"💥 {enemy.name} attacks {character.nickname} and deals {damage_to_character_cp} CP damage. {character.nickname} has {character_cp} CP left.\n"
                else:
                    damage_to_character_hp = math.floor(min(enemy.get_dmg(), character_hp))
                    character_hp -= damage_to_character_hp
                    battle_log = f"💥 {enemy.name} attacks {character.nickname} and deals {damage_to_character_hp} HP damage. {character.nickname} has {character_hp} HP left.\n"

            bot.send_message(chat_id, battle_log)
            time.sleep(1)

            if character_hp == 0:
                battle_log = f"☠️ {character.nickname} has been defeated!\n"
                bot.send_message(chat_id, battle_log)
                # Если персонаж проиграл, дать 25% опыта
                exp_gain = math.ceil(total_exp * 0.25)
                character.add_experience(exp_gain)
                final_exp = character.exp
                level = character.level
                bot.send_message(chat_id, f"🏆 Adding experience: {exp_gain}, current experience: {final_exp}")
                bot.send_message(chat_id, f"📈 Final experience: {final_exp}, level: {level}")
                reset_effects(character, original_methods)  # Сбрасываем эффекты после боя
                return

    if character_hp > 0:
        battle_won = True

    if battle_won:
        battle_log = f"🎉 {character.nickname} has defeated all enemies!\n"
        bot.send_message(chat_id, battle_log)
        # Если персонаж победил, дать полный опыт
        exp_gain = math.ceil(total_exp)
        character.add_experience(exp_gain)
        final_exp = character.exp
        level = character.level
        bot.send_message(chat_id, f"🏆 Adding experience: {exp_gain}, current experience: {final_exp}")
        bot.send_message(chat_id, f"📈 Final experience: {final_exp}, level: {level}")

    reset_effects(character, original_methods)  # Сбрасываем эффекты после боя
