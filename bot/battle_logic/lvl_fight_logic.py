import time
import random
import math
from bot.management.commands.game_dice import apply_random_effect, reset_effects
from bot.models import Character
from bot.enemies import Enemy
from bot.battle_logic.boss_skills import *
from bot.battle_logic.hero_skills import *


def battle(bot, chat_id, character, enemies):
    original_methods = {'calculate_dodge': character.calculate_dodge}
    apply_random_effect(character)
    bot.send_message(chat_id, f"🎲 Random effect applied: {character.effects}")
    # time.sleep(1)

    character_hp = character.hp
    character_cp = character.cp
    battle_log = f"⚔️ Battle between {character.nickname} and enemies has begun! ⚔️\n"
    bot.send_message(chat_id, battle_log)
    # time.sleep(1)

    total_exp = 0

    # Variables for Regenerate/Lose health effects
    regenerate_amount = character.regenerate_amount if hasattr(character, 'regenerate_amount') else 0
    lose_health_amount = character.lose_health_amount if hasattr(character, 'lose_health_amount') else 0

    for enemy in enemies:
        enemy_hp = enemy.get_hp()
        enemy_cp = enemy.get_cp()
        total_exp += enemy.exp_reward

        while character_hp > 0 and (enemy_hp > 0 or enemy_cp > 0):
            # Apply Regenerate/Lose health effects
            if character.regenerate:
                regenerate_hp = math.ceil(regenerate_amount)
                character_hp = min(character.hp, character_hp + regenerate_hp)
                bot.send_message(chat_id,
                                 f"🌿 {character.nickname} regenerates {regenerate_hp} HP. {character.nickname} has {character_hp} HP now.")

            if character.lose_health:
                lose_hp = math.ceil(lose_health_amount)
                character_hp = max(0, character_hp - lose_hp)
                bot.send_message(chat_id,
                                 f"💔 {character.nickname} loses {lose_hp} HP. {character.nickname} has {character_hp} HP now.")

            # Character uses skill or attacks enemy
            if character.effects != 'rooted':
                if character.skills.get("root") and random.random() < 0.5:  # 50% chance to use 'root'
                    hero_use_skill(character, "root", enemy, bot, chat_id)
                elif random.random() < (character.calculate_crit_chance() / 100):
                    crit_dmg = character.calculate_crit()
                    if enemy_cp > 0:
                        damage_to_enemy_cp = math.ceil(min(crit_dmg, enemy_cp))
                        enemy_cp -= damage_to_enemy_cp
                        battle_log = f"💥 {character.nickname} crits {enemy.name} for {damage_to_enemy_cp} CP. {enemy.enemy_type} has {enemy_cp} CP left.\n"
                    else:
                        damage_to_enemy_hp = math.ceil(min(crit_dmg, enemy_hp))
                        enemy_hp -= damage_to_enemy_hp
                        battle_log = f"💥 {character.nickname} crits {enemy.name} for {damage_to_enemy_hp} HP. {enemy.enemy_type} has {enemy_hp} HP left.\n"
                else:
                    if enemy_cp > 0:
                        damage_to_enemy_cp = math.ceil(min(character.dmg, enemy_cp))
                        enemy_cp -= damage_to_enemy_cp
                        battle_log = f"⚔️ {character.nickname} attacks {enemy.name} for {damage_to_enemy_cp} CP. {enemy.enemy_type} has {enemy_cp} CP left.\n"
                    else:
                        damage_to_enemy_hp = math.ceil(min(character.dmg, enemy_hp))
                        enemy_hp -= damage_to_enemy_hp
                        battle_log = f"⚔️ {character.nickname} attacks {enemy.name} for {damage_to_enemy_hp} HP. {enemy.enemy_type} has {enemy_hp} HP left.\n"

                bot.send_message(chat_id, battle_log)
                # time.sleep(1)
            else:
                bot.send_message(chat_id, f"{character.nickname} is rooted and cannot attack.")
                # time.sleep(1)

            if enemy_hp == 0 and enemy_cp == 0:
                battle_log = f"☠️ {enemy.name} defeated!\n"
                bot.send_message(chat_id, battle_log)
                # time.sleep(1)
                if "root" in enemy.skills:
                    character.skills["root"] = True
                    battle_log = f"🎉 {character.nickname} has learned the 'root' skill from {enemy.name}!\n"
                    bot.send_message(chat_id, battle_log)
                break

            # Enemy uses skill or attacks character
            if enemy.skills.get("root") and random.random() < 1:  # 100% chance to use 'root'
                boss_use_skill(enemy, "root", character, bot, chat_id)
            elif random.random() < (character.calculate_dodge() / 100):
                battle_log = f"🛡️ {character.nickname} dodges {enemy.name}'s attack!\n"
            else:
                if character_cp > 0:
                    damage_to_character_cp = math.floor(min(enemy.get_dmg(), character_cp))
                    character_cp -= damage_to_character_cp
                    battle_log = f"💥 {enemy.name} attacks {character.nickname} for {damage_to_character_cp} CP. {character.nickname} has {character_cp} CP left.\n"
                else:
                    damage_to_character_hp = math.floor(min(enemy.get_dmg(), character_hp))
                    character_hp -= damage_to_character_hp
                    battle_log = f"💥 {enemy.name} attacks {character.nickname} for {damage_to_character_hp} HP. {character.nickname} has {character_hp} HP left.\n"

            bot.send_message(chat_id, battle_log)
            # time.sleep(1)

            if character_hp == 0:
                battle_log = f"☠️ {character.nickname} defeated!\n"
                bot.send_message(chat_id, battle_log)
                exp_gain = math.ceil(total_exp * 0.25)
                character.add_experience(exp_gain)
                final_exp = character.exp
                level = character.level
                bot.send_message(chat_id, f"🏆 Exp gained: {exp_gain}, Total exp: {final_exp}, Level: {level}")
                reset_effects(character, original_methods)
                character.in_battle = False
                character.save()
                return

    battle_won = False
    if character_hp > 0:
        battle_won = True

    if battle_won:
        state_parts = character.state.split('_')
        location = '_'.join(state_parts[:2])
        current_level = int(state_parts[-1])

        print(f"Current location: {location}, Current level: {current_level}")  # Отладочное сообщение

        if location == 'location_1':
            character.completed_forest_levels += 1
            character.current_forest_level = current_level + 1
            character.state = f'location_1_level_{character.current_forest_level}'
            print(f"New forest level: {character.current_forest_level}")  # Отладочное сообщение
            character.save()
        elif location == 'location_2':
            character.completed_catacombs_levels += 1
            character.current_catacombs_level = current_level + 1
            character.state = f'location_2_level_{character.current_catacombs_level}'
            print(f"New catacombs level: {character.current_catacombs_level}")  # Отладочное сообщение
        elif location == 'location_3':
            character.completed_magma_levels += 1
            character.current_magma_level = current_level + 1
            character.state = f'location_3_level_{character.current_magma_level}'
            print(f"New magma level: {character.current_magma_level}")  # Отладочное сообщение

        if character.completed_forest_levels >= 10 and character.completed_catacombs_levels >= 10 and character.completed_magma_levels >= 10:
            character.completed_locations += 1

        character.in_battle = False
        character.save()

        print(f"User state after winning the battle: {character.state}")  # Отладочное сообщение

        battle_log = f"🎉 {character.nickname} defeated all enemies in level {current_level}!\n"
        bot.send_message(chat_id, battle_log)

        exp_gain = math.ceil(total_exp)
        character.add_experience(exp_gain)
        final_exp = character.exp
        level = character.level
        bot.send_message(chat_id, f"🏆 Exp gained: {exp_gain}, Total exp: {final_exp}, Level: {level}")

    reset_effects(character, original_methods)
