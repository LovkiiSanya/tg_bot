from bot.models import Character
from bot.enemies import Enemy
import random
import time
import math


def hero_use_skill(character, skill_name, target, bot, chat_id):
    if skill_name == "root" and character.skills.get("root") and random.random() <= 0.2:
        if not target.get_skill_effects().get('rooted'):  # Check if not already rooted
            target.add_skill_effect('rooted')

            if isinstance(target, Character):
                target_name = target.nickname
            elif isinstance(target, Enemy):
                target_name = target.name
            else:
                target_name = "Unknown"

            bot.send_message(chat_id,
                             f"{character.nickname} uses 'root' on {target_name}. {target_name} cannot attack for 3 "
                             f"turns.")

            # Logic for handling root for 3 turns
            for turn in range(3):
                if isinstance(target, Character) and target.hp <= 0:
                    break
                elif isinstance(target, Enemy) and target.base_hp <= 0:
                    break

                if target.get_skill_effects().get('rooted'):  # Ensure target is rooted
                    # Character attacks during root effect
                    if random.random() < (character.calculate_crit_chance() / 100):
                        crit_dmg = character.calculate_crit()
                        if target.base_cp > 0:
                            damage_to_target_cp = math.ceil(min(crit_dmg, target.base_cp))
                            target.base_cp -= damage_to_target_cp
                            battle_log = f"💥 {character.nickname} crits {target_name} for {damage_to_target_cp} CP. {target_name} has {target.base_cp} CP left.\n"
                        else:
                            damage_to_target_hp = math.ceil(min(crit_dmg, target.base_hp))
                            target.base_hp -= damage_to_target_hp
                            battle_log = f"💥 {character.nickname} crits {target_name} for {damage_to_target_hp} HP. {target_name} has {target.base_hp} HP left.\n"
                    else:
                        if target.base_cp > 0:
                            damage_to_target_cp = math.ceil(min(character.dmg, target.base_cp))
                            target.base_cp -= damage_to_target_cp
                            battle_log = f"⚔️ {character.nickname} attacks {target_name} for {damage_to_target_cp} CP. {target_name} has {target.base_cp} CP left.\n"
                        else:
                            damage_to_target_hp = math.ceil(min(character.dmg, target.base_hp))
                            target.base_hp -= damage_to_target_hp
                            battle_log = f"⚔️ {character.nickname} attacks {target_name} for {damage_to_target_hp} HP. {target_name} has {target.base_hp} HP left.\n"

                    bot.send_message(chat_id, battle_log)
                    time.sleep(1)
                    bot.send_message(chat_id, f"Turn {turn + 1}: {target_name} still cannot attack.")
                    time.sleep(1)

            target.remove_skill_effect('rooted')

        else:
            bot.send_message(chat_id, f"already rooted and cannot be affected again.")

    else:
        bot.send_message(chat_id, f"{character.nickname} attempts to use 'root' but the skill fails to activate.")
