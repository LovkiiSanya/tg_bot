from bot.models import Character
from bot.enemies import Enemy
import random
import time


def boss_use_skill(enemy, skill_name, target, bot, chat_id):
    if isinstance(target, Character):
        target_name = target.nickname
    elif isinstance(target, Enemy):
        target_name = target.name
    else:
        target_name = "Unknown"

    if skill_name == "root" and enemy.skills.get("root") and random.random() <= 0.5:  # 50% chance to use the skill
        if not target.get_skill_effects().get('rooted'):
            target.add_skill_effect('rooted')

            bot.send_message(chat_id,
                             f"{enemy.name} uses 'root' on {target_name}. {target_name} cannot attack for 3 turns.")

            # Logic for handling root for 3 turns
            for turn in range(3):
                if isinstance(target, Character) and target.hp <= 0:
                    break
                elif isinstance(target, Enemy) and target.base_hp <= 0:
                    break

                if target.get_skill_effects().get('rooted'):  # Ensure target is rooted
                    # Boss attacks during root effect
                    if random.random() < 0.25:  # Assuming 25% crit chance for boss
                        crit_dmg = enemy.base_dmg * 2  # Assuming crit is double damage for boss
                        if target.cp > 0:
                            damage_to_target_cp = min(crit_dmg, target.cp)
                            target.cp -= damage_to_target_cp
                            battle_log = f"💥 {enemy.name} crits {target_name} for {damage_to_target_cp} CP. {target_name} has {target.cp} CP left.\n"
                        else:
                            damage_to_target_hp = min(crit_dmg, target.hp)
                            target.hp -= damage_to_target_hp
                            battle_log = f"💥 {enemy.name} crits {target_name} for {damage_to_target_hp} HP. {target_name} has {target.hp} HP left.\n"
                    else:
                        if target.cp > 0:
                            damage_to_target_cp = min(enemy.base_dmg, target.cp)
                            target.cp -= damage_to_target_cp
                            battle_log = f"⚔️ {enemy.name} attacks {target_name} for {damage_to_target_cp} CP. {target_name} has {target.cp} CP left.\n"
                        else:
                            damage_to_target_hp = min(enemy.base_dmg, target.hp)
                            target.hp -= damage_to_target_hp
                            battle_log = f"⚔️ {enemy.name} attacks {target_name} for {damage_to_target_hp} HP. {target_name} has {target.hp} HP left.\n"

                    bot.send_message(chat_id, battle_log)
                    time.sleep(1)
                    bot.send_message(chat_id, f"Turn {turn + 1}: {target_name} still cannot attack.")
                    time.sleep(1)

            target.remove_skill_effect('rooted')

            if isinstance(enemy, Enemy) and enemy.base_hp <= 0:
                target.skills["root"] = True
                target.save()
                bot.send_message(chat_id, f"{target_name} has learned the 'root' skill from defeating {enemy.name}.")
        else:
            bot.send_message(chat_id, f"{target_name} is already rooted and cannot be affected again.")
    else:
        # Boss attacks normally if the skill doesn't activate
        if random.random() < 0.25:  # Assuming 25% crit chance for boss
            crit_dmg = enemy.base_dmg * 2  # Assuming crit is double damage for boss
            if target.cp > 0:
                damage_to_target_cp = min(crit_dmg, target.cp)
                target.cp -= damage_to_target_cp
                battle_log = f"💥 {enemy.name} crits {target_name} for {damage_to_target_cp} CP. {target_name} has {target.cp} CP left.\n"
            else:
                damage_to_target_hp = min(crit_dmg, target.hp)
                target.hp -= damage_to_target_hp
                battle_log = f"💥 {enemy.name} crits {target_name} for {damage_to_target_hp} HP. {target_name} has {target.hp} HP left.\n"
        else:
            if target.cp > 0:
                damage_to_target_cp = min(enemy.base_dmg, target.cp)
                target.cp -= damage_to_target_cp
                battle_log = f"⚔️ {enemy.name} attacks {target_name} for {damage_to_target_cp} CP. {target_name} has {target.cp} CP left.\n"
            else:
                damage_to_target_hp = min(enemy.base_dmg, target.hp)
                target.hp -= damage_to_target_hp
                battle_log = f"⚔️ {enemy.name} attacks {target_name} for {damage_to_target_hp} HP. {target_name} has {target.hp} HP left.\n"

        bot.send_message(chat_id, battle_log)
