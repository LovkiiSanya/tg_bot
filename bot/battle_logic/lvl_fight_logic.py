import math
import random
import time
from bot.management.commands.game_dice import apply_random_effect, reset_effects
from bot.battle_logic.boss_skills import boss_use_skill
from bot.battle_logic.hero_skills import hero_use_skill
import logging

logging.basicConfig(level=logging.INFO)


def battle(bot, chat_id, character, enemies):
    original_methods = {"calculate_dodge": character.calculate_dodge}
    apply_random_effect(character)
    bot.send_message(chat_id, "🎲 Random effect applied: {}".format(character.effects))

    character_hp = character.hp
    character_cp = character.cp
    battle_log = "⚔️ Battle between {} and enemies has begun! ⚔️\n".format(character.nickname)
    bot.send_message(chat_id, battle_log)

    total_exp = 0
    regenerate_amount = getattr(character, "regenerate_amount", 0)
    lose_health_amount = getattr(character, "lose_health_amount", 0)

    for enemy in enemies:
        enemy_hp = enemy.get_hp()
        enemy_cp = enemy.get_cp()
        total_exp += enemy.exp_reward

        while character_hp > 0 and (enemy_hp > 0 or enemy_cp > 0):
            # Regeneration
            if character.regenerate:
                regenerate_hp = math.ceil(regenerate_amount)
                character_hp = min(character.hp, character_hp + regenerate_hp)
                bot.send_message(chat_id,
                                 "{} regenerates {} HP. {} has {} HP now.".format(character.nickname, regenerate_hp,
                                                                                  character.nickname, character_hp))

            # Losing health
            if character.lose_health:
                lose_hp = math.ceil(lose_health_amount)
                character_hp = max(0, character_hp - lose_hp)
                bot.send_message(chat_id, "{} loses {} HP. {} has {} HP now.".format(character.nickname, lose_hp,
                                                                                     character.nickname, character_hp))

            if character_hp <= 0:  # Check after losing health
                break

            # Character's attack
            if character.effects != "rooted":
                if character.skills.get("root") and random.random() < 0.5:
                    hero_use_skill(character, "root", enemy, bot, chat_id)
                elif random.random() < (character.calculate_crit_chance() / 100):
                    crit_dmg = character.calculate_crit()
                    if enemy_cp > 0:
                        damage_to_enemy_cp = math.ceil(min(crit_dmg, enemy_cp))
                        enemy_cp -= damage_to_enemy_cp
                        battle_log = "{} crits {} for {} CP. {} has {} CP left.\n".format(character.nickname,
                                                                                          enemy.name,
                                                                                          damage_to_enemy_cp,
                                                                                          enemy.enemy_type, enemy_cp)
                    else:
                        damage_to_enemy_hp = math.ceil(min(crit_dmg, enemy_hp))
                        enemy_hp -= damage_to_enemy_hp
                        battle_log = "{} crits {} for {} HP. {} has {} HP left.\n".format(character.nickname,
                                                                                          enemy.name,
                                                                                          damage_to_enemy_hp,
                                                                                          enemy.enemy_type, enemy_hp)
                else:
                    if enemy_cp > 0:
                        damage_to_enemy_cp = math.ceil(min(character.dmg, enemy_cp))
                        enemy_cp -= damage_to_enemy_cp
                        battle_log = "{} attacks {} for {} CP. {} has {} CP left.\n".format(character.nickname,
                                                                                            enemy.name,
                                                                                            damage_to_enemy_cp,
                                                                                            enemy.enemy_type, enemy_cp)
                    else:
                        damage_to_enemy_hp = math.ceil(min(character.dmg, enemy_hp))
                        enemy_hp -= damage_to_enemy_hp
                        battle_log = "{} attacks {} for {} HP. {} has {} HP left.\n".format(character.nickname,
                                                                                            enemy.name,
                                                                                            damage_to_enemy_hp,
                                                                                            enemy.enemy_type, enemy_hp)

                bot.send_message(chat_id, battle_log)
            else:
                bot.send_message(chat_id, "{} is rooted and cannot attack.".format(character.nickname))

            # Check if enemy is defeated
            if enemy_hp <= 0 and enemy_cp <= 0:
                battle_log = "{} defeated!\n".format(enemy.name)
                bot.send_message(chat_id, battle_log)
                if "root" in enemy.skills:
                    character.skills["root"] = True
                    bot.send_message(chat_id, "{} has learned the 'root' skill from {}!\n".format(character.nickname,
                                                                                                  enemy.name))
                break

            # Enemy's attack
            if enemy.skills.get("root") and random.random() < 1:
                boss_use_skill(enemy, "root", character, bot, chat_id)
            elif random.random() < (character.calculate_dodge() / 100):
                bot.send_message(chat_id, "{} dodges {}'s attack!\n".format(character.nickname, enemy.name))
            else:
                if character_cp > 0:
                    damage_to_character_cp = math.floor(min(enemy.get_dmg(), character_cp))
                    character_cp -= damage_to_character_cp
                    battle_log = "{} attacks {} for {} CP. {} has {} CP left.\n".format(enemy.name, character.nickname,
                                                                                        damage_to_character_cp,
                                                                                        character.nickname,
                                                                                        character_cp)
                else:
                    damage_to_character_hp = math.floor(min(enemy.get_dmg(), character_hp))
                    character_hp -= damage_to_character_hp
                    battle_log = "{} attacks {} for {} HP. {} has {} HP left.\n".format(enemy.name, character.nickname,
                                                                                        damage_to_character_hp,
                                                                                        character.nickname,
                                                                                        character_hp)

                bot.send_message(chat_id, battle_log)

            # Check if character is defeated
            if character_hp <= 0:
                battle_log = "{} defeated!\n".format(character.nickname)
                bot.send_message(chat_id, battle_log)
                exp_gain = math.ceil(total_exp * 0.25)
                character.add_experience(exp_gain)
                final_exp = character.exp
                level = character.level
                bot.send_message(chat_id,
                                 "🏆 Exp gained: {}, Total exp: {}, Level: {}".format(exp_gain, final_exp, level))
                reset_effects(character, original_methods)
                character.in_battle = False
                character.save()
                return

    # If the character is still alive after all enemies
    if character_hp > 0:
        state_parts = character.state.split("_")
        location = "_".join(state_parts[:2])
        current_level = int(state_parts[-1])

        if location == "location_1":
            character.completed_forest_levels += 1
            character.current_forest_level = current_level + 1
            character.state = "location_1_level_{}".format(character.current_forest_level)
            character.save()
        elif location == "location_2":
            character.completed_catacombs_levels += 1
            character.current_catacombs_level = current_level + 1
            character.state = "location_2_level_{}".format(character.current_catacombs_level)
            character.save()
        elif location == "location_3":
            character.completed_magma_levels += 1
            character.current_magma_level = current_level + 1
            character.state = "location_3_level_{}".format(character.current_magma_level)
            character.save()

        if (character.completed_forest_levels >= 10 and
                character.completed_catacombs_levels >= 10 and
                character.completed_magma_levels >= 10):
            character.completed_locations += 1

        character.in_battle = False
        character.save()

        logging.info("User state after winning the battle: {}".format(character.state))

        battle_log = "🎉 {} defeated all enemies in level {}!\n".format(character.nickname, current_level)
        bot.send_message(chat_id, battle_log)

        exp_gain = math.ceil(total_exp)
        character.add_experience(exp_gain)
        final_exp = character.exp
        level = character.level
        bot.send_message(chat_id, "🏆 Exp gained: {}, Total exp: {}, Level: {}".format(exp_gain, final_exp, level))

    reset_effects(character, original_methods)
