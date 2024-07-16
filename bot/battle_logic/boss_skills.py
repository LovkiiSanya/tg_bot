import random

from bot.models import Character
from bot.enemies import EnemyModel
import time


def boss_use_skill(enemy, skill_name, target, bot, chat_id):
    if isinstance(target, Character):
        target_name = target.nickname
    elif isinstance(target, EnemyModel):
        target_name = target.name
    else:
        target_name = "Unknown"

    if skill_name == "root" and enemy.skills.get("root") and random.random() <= 0.5:
        if not target.get_skill_effects().get("rooted"):
            target.add_skill_effect("rooted")
            bot.send_message(
                chat_id,
                "{} uses 'root' on {}. {} cannot attack for 3 turns.".format(
                    enemy.name, target_name, target_name
                ),
            )

            for turn in range(3):
                if (
                    isinstance(target, Character) and target.hp <= 0
                ) or (
                    isinstance(target, EnemyModel) and target.base_hp <= 0
                ):
                    break

                if target.get_skill_effects().get("rooted"):
                    if random.random() < 0.25:
                        crit_dmg = enemy.base_dmg * 2
                        if target.cp > 0:
                            damage_to_target_cp = min(crit_dmg, target.cp)
                            target.cp -= damage_to_target_cp
                            battle_log = (
                                "💥 {} crits {} for {} CP. {} has {} CP left.\n".format(
                                    enemy.name,
                                    target_name,
                                    damage_to_target_cp,
                                    target_name,
                                    target.cp,
                                )
                            )
                        else:
                            damage_to_target_hp = min(crit_dmg, target.hp)
                            target.hp -= damage_to_target_hp
                            battle_log = (
                                "💥 {} crits {} for {} HP. {} has {} HP left.\n".format(
                                    enemy.name,
                                    target_name,
                                    damage_to_target_hp,
                                    target_name,
                                    target.hp,
                                )
                            )
                    else:
                        if target.cp > 0:
                            damage_to_target_cp = min(enemy.base_dmg, target.cp)
                            target.cp -= damage_to_target_cp
                            battle_log = (
                                "⚔️ {} attacks {} for {} CP. {} has {} CP left.\n".format(
                                    enemy.name,
                                    target_name,
                                    damage_to_target_cp,
                                    target_name,
                                    target.cp,
                                )
                            )
                        else:
                            damage_to_target_hp = min(enemy.base_dmg, target.hp)
                            target.hp -= damage_to_target_hp
                            battle_log = (
                                "⚔️ {} attacks {} for {} HP. {} has {} HP left.\n".format(
                                    enemy.name,
                                    target_name,
                                    damage_to_target_hp,
                                    target_name,
                                    target.hp,
                                )
                            )

                    bot.send_message(chat_id, battle_log)
                    time.sleep(1)
                    bot.send_message(
                        chat_id,
                        "Turn {}: {} still cannot attack.".format(turn + 1, target_name),
                    )
                    time.sleep(1)

            target.remove_skill_effect("rooted")

            if isinstance(enemy, EnemyModel) and enemy.base_hp <= 0:
                target.skills["root"] = True
                target.save()
                bot.send_message(
                    chat_id,
                    "{} has learned the 'root' skill from defeating {}.".format(
                        target_name, enemy.name
                    ),
                )
        else:
            bot.send_message(
                chat_id,
                "{} is already rooted and cannot be affected again.".format(
                    target_name,
                ),
            )
    else:
        if random.random() < 0.25:
            crit_dmg = enemy.base_dmg * 2
            if target.cp > 0:
                damage_to_target_cp = min(crit_dmg, target.cp)
                target.cp -= damage_to_target_cp
                battle_log = (
                    "💥 {} crits {} for {} CP. {} has {} CP left.\n".format(
                        enemy.name,
                        target_name,
                        damage_to_target_cp,
                        target_name,
                        target.cp,
                    )
                )
            else:
                damage_to_target_hp = min(crit_dmg, target.hp)
                target.hp -= damage_to_target_hp
                battle_log = (
                    "💥 {} crits {} for {} HP. {} has {} HP left.\n".format(
                        enemy.name,
                        target_name,
                        damage_to_target_hp,
                        target_name,
                        target.hp,
                    )
                )
        else:
            if target.cp > 0:
                damage_to_target_cp = min(enemy.base_dmg, target.cp)
                target.cp -= damage_to_target_cp
                battle_log = (
                    "⚔️ {} attacks {} for {} CP. {} has {} CP left.\n".format(
                        enemy.name,
                        target_name,
                        damage_to_target_cp,
                        target_name,
                        target.cp,
                    )
                )
            else:
                damage_to_target_hp = min(enemy.base_dmg, target.hp)
                target.hp -= damage_to_target_hp
                battle_log = (
                    "⚔️ {} attacks {} for {} HP. {} has {} HP left.\n".format(
                        enemy.name,
                        target_name,
                        damage_to_target_hp,
                        target_name,
                        target.hp,
                    )
                )

        bot.send_message(chat_id, battle_log)
