
import random


def apply_random_effect(character):
    effects = [
        "Double Damage",
        "Weaken opponents (-10% attack)",
        "Increase health by 20%",
        "Disable dodge",
        "Damage reduction by 10%"
    ]
    effect = random.choice(effects)
    character.effects = effect

    if effect == "Double Damage":
        character.dmg *= 2
    elif effect == "Weaken opponents (-10% attack)":
        pass  # Реализуйте логику ослабления противников
    elif effect == "Increase health by 20%":
        character.hp *= 1.2
    elif effect == "Disable dodge":
        character.calculate_dodge = lambda: 0
    elif effect == "Damage reduction by 10%":
        character.dmg *= 0.9

    character.save()
