import random
from bot.enemies import Enemy


def apply_random_effect(character):
    effects = {
        "Double Damage": lambda: setattr(character, 'dmg', character.dmg * 2),
        "Weaken opponents (-10% attack)": lambda: weaken_enemies(),
        "Increase health by 20%": lambda: setattr(character, 'hp', int(character.hp * 1.2)),
        "Disable dodge": lambda: setattr(character, 'dodge_modifier', -character.calculate_dodge()),
        "Damage reduction by 10%": lambda: setattr(character, 'dmg', int(character.dmg * 0.9)),
        "Increase damage by 15%": lambda: setattr(character, 'dmg', int(character.dmg * 1.15)),
        "Reduce damage by 15%": lambda: setattr(character, 'dmg', int(character.dmg * 0.85)),
        "Increase dodge by 20%": lambda: setattr(character, 'dodge_modifier', character.dodge_modifier + 20),
        "Reduce dodge by 20%": lambda: setattr(character, 'dodge_modifier', max(0, character.dodge_modifier - 20)),
        "Increase critical hit chance by 10%": lambda: setattr(character, 'crit_chance_modifier',
                                                               character.crit_chance_modifier + 0.1),
        "Reduce critical hit chance by 10%": lambda: setattr(character, 'crit_chance_modifier',
                                                             max(0, character.crit_chance_modifier - 0.1)),
        "Regenerate 5% health each turn": lambda: setattr(character, 'regenerate', True),
        "Lose 5% health each turn": lambda: (
            setattr(character, 'lose_health', True),
            setattr(character, 'lose_health_amount', int(0.05 * character.hp))
        ),
        "Increase CP by 10%": lambda: setattr(character, 'cp', int(character.cp * 1.1)),
        "Reduce CP by 10%": lambda: setattr(character, 'cp', int(character.cp * 0.9)),
    }

    effect = random.choice(list(effects.keys()))
    character.effects = effect

    effects[effect]()

    character.save()


def reset_effects(character, original_methods):
    effects_reset = {
        "Double Damage": lambda: setattr(character, 'dmg', character.dmg // 2),
        "Weaken opponents (-10% attack)": lambda: unweaken_enemies(),
        "Increase health by 20%": lambda: setattr(character, 'hp', int(character.hp // 1.2)),
        "Disable dodge": lambda: setattr(character, 'dodge_modifier', 0),
        "Damage reduction by 10%": lambda: setattr(character, 'dmg', int(character.dmg // 0.9)),
        "Increase damage by 15%": lambda: setattr(character, 'dmg', int(character.dmg // 1.15)),
        "Reduce damage by 15%": lambda: setattr(character, 'dmg', int(character.dmg // 0.85)),
        "Increase dodge by 20%": lambda: setattr(character, 'dodge_modifier', character.dodge_modifier - 20),
        "Reduce dodge by 20%": lambda: setattr(character, 'dodge_modifier', max(0, character.dodge_modifier + 20)),
        "Increase critical hit chance by 10%": lambda: setattr(character, 'crit_chance_modifier',
                                                               character.crit_chance_modifier - 0.1),
        "Reduce critical hit chance by 10%": lambda: setattr(character, 'crit_chance_modifier',
                                                             max(0, character.crit_chance_modifier + 0.1)),
        "Regenerate 5% health each turn": lambda: (
            setattr(character, 'regenerate', False),
            setattr(character, 'regenerate_amount', 0)
        ),
        "Lose 5% health each turn": lambda: (
            setattr(character, 'lose_health', False),
            setattr(character, 'lose_health_amount', 0)
        ),
        "Increase CP by 10%": lambda: setattr(character, 'cp', int(character.cp // 1.1)),
        "Reduce CP by 10%": lambda: setattr(character, 'cp', int(character.cp // 0.9)),
    }

    reset_action = effects_reset.get(character.effects, lambda: None)
    reset_action()

    character.effects = ''
    character.save()


def weaken_enemies():
    for enemy in Enemy.objects.all():
        enemy.weaken()


def unweaken_enemies():
    for enemy in Enemy.objects.all():
        enemy.unweaken()
