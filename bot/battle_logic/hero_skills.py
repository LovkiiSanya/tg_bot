import math
import random

from bot.models import Character
from bot.enemies import EnemyModel
import time


def hero_use_skill(character, skill_name, target, bot, chat_id):
    if skill_name == "root" and character.skills.get("root") and random.random() <= 0.2:
        if isinstance(target, Character):
            target_name = target.nickname
        elif isinstance(target, EnemyModel):
            target_name = target.name
        else:
            target_name = "Unknown"

        if not target.get_skill_effects().get("rooted"):
            target.add_skill_effect("rooted")

            bot.send_message(
                chat_id,
                "{} uses 'root' on {}. {} cannot attack for 3 turns.".format(
                    character.nickname, target_name, target_name
                ),
            )

            for turn in range(3):
                if isinstance(target, Character) and target.hp <= 0:
                    break
                elif isinstance(target, EnemyModel) and target.base_hp <= 0:
                    break

                if target.get_skill_effects().get("rooted"):
                    if random.random() < (character.calculate_crit_chance() / 100):
                        crit_dmg = character.calculate_crit()
                        if target.base_cp > 0:
                            damage_to_target_cp = math.ceil(min(crit_dmg, target.base_cp))
                            target.base_cp -= damage_to_target_cp
                            battle_log = (
                                "💥 {} crits {} for {} CP. {} has {} CP left.\n".format(
                                    character.nickname,
                                    target_name,
                                    damage_to_target_cp,
                                    target_name,
                                    target.base_cp,
                                )
                            )
                        else:
                            damage_to_target_hp = math.ceil(min(crit_dmg, target.base_hp))
                            target.base_hp -= damage_to_target_hp
                            battle_log = (
                                "💥 {} crits {} for {} HP. {} has {} HP left.\n".format(
                                    character.nickname,
                                    target_name,
                                    damage_to_target_hp,
                                    target_name,
                                    target.base_hp,
                                )
                            )
                    else:
                        if target.base_cp > 0:
                            damage_to_target_cp = math.ceil(
                                min(character.dmg, target.base_cp)
                            )
                            target.base_cp -= damage_to_target_cp
                            battle_log = (
                                "⚔️ {} attacks {} for {} CP. {} has {} CP left.\n".format(
                                    character.nickname,
                                    target_name,
                                    damage_to_target_cp,
                                    target_name,
                                    target.base_cp,
                                )
                            )
                        else:
                            damage_to_target_hp = math.ceil(
                                min(character.dmg, target.base_hp)
                            )
                            target.base_hp -= damage_to_target_hp
                            battle_log = (
                                "⚔️ {} attacks {} for {} HP. {} has {} HP left.\n".format(
                                    character.nickname,
                                    target_name,
                                    damage_to_target_hp,
                                    target_name,
                                    target.base_hp,
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

        else:
            bot.send_message(
                chat_id,
                "{} is already rooted and cannot be affected again.".format(target_name),
            )

    else:
        bot.send_message(
            chat_id,
            "{} attempts to use 'root' but the skill fails to activate.".format(
                character.nickname
            ),
        )
