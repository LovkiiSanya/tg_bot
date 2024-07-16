import json
from django.db import models

# Constants
MAX_NAME_LENGTH = 50
DEFAULT_BASE_HP = 100
DEFAULT_BASE_CP = 10
DEFAULT_BASE_DMG = 10
DEFAULT_LEVEL = 1
DEFAULT_ENEMY_TYPE = "Generic"
DEFAULT_EXP_REWARD = 50
DEFAULT_WEAKENED = False
DEFAULT_SKILLS = dict()
MAX_EFFECTS_LENGTH = 255
DEFAULT_SKILL_EFFECTS = "{}"
WEAKENED_DAMAGE_MULTIPLIER = 0.9

GOBLIN_HP = 50
GOBLIN_DMG = 5
GOBLIN_CP = 0
GOBLIN_EXP = 50

SKELETON_HP = 100
SKELETON_DMG = 25
SKELETON_CP = 10
SKELETON_EXP = 100

SHADOW_HP = 80
SHADOW_DMG = 30
SHADOW_CP = 15
SHADOW_EXP = 120

COBALT_HP = 80
COBALT_DMG = 30
COBALT_CP = 15
COBALT_EXP = 120

WOLF_HP = 10
WOLF_DMG = 20
WOLF_CP = 5
WOLF_EXP = 100

ORC_HP = 15
ORC_DMG = 25
ORC_CP = 15
ORC_EXP = 200

GOLEM_HP = 40
GOLEM_DMG = 20
GOLEM_CP = 7
GOLEM_EXP = 2500

CERBERUS_HP = 100
CERBERUS_DMG = 20
CERBERUS_CP = 5
CERBERUS_EXP = 100

HYDRA_HP = 100
HYDRA_DMG = 20
HYDRA_CP = 5
HYDRA_EXP = 100

DRAGON_HP = 1000
DRAGON_DMG = 100
DRAGON_CP = 250
DRAGON_EXP = 500

BOSS_FAIRY_HP = 800
BOSS_FAIRY_DMG = 100
BOSS_FAIRY_CP = 25
BOSS_FAIRY_EXP = 1000

BOSS_BEAR_HP = 80
BOSS_BEAR_DMG = 100
BOSS_BEAR_CP = 25
BOSS_BEAR_EXP = 5000

BOSS_PHOENIX_HP = 800
BOSS_PHOENIX_DMG = 100
BOSS_PHOENIX_CP = 25
BOSS_PHOENIX_EXP = 1000


class EnemyModel(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    base_hp = models.IntegerField(default=DEFAULT_BASE_HP)
    base_cp = models.IntegerField(default=DEFAULT_BASE_CP)
    base_dmg = models.IntegerField(default=DEFAULT_BASE_DMG)
    level = models.IntegerField(default=DEFAULT_LEVEL)
    enemy_type = models.CharField(max_length=MAX_NAME_LENGTH, default=DEFAULT_ENEMY_TYPE)
    exp_reward = models.IntegerField(default=DEFAULT_EXP_REWARD)
    weakened = models.BooleanField(default=DEFAULT_WEAKENED)
    skills = models.JSONField(default=dict, blank=True)
    effects = models.CharField(max_length=MAX_EFFECTS_LENGTH, null=True, blank=True)
    skill_effects = models.TextField(default=DEFAULT_SKILL_EFFECTS)

    def get_skill_effects(self):
        try:
            return json.loads(self.skill_effects)
        except json.JSONDecodeError:
            return {}

    def add_skill_effect(self, effect_name):
        effects = self.get_skill_effects()
        effects[effect_name] = True
        self.skill_effects = json.dumps(effects)
        self.save()

    def remove_skill_effect(self, effect_name):
        effects = self.get_skill_effects()
        if effect_name in effects:
            effects.pop(effect_name, None)
            self.skill_effects = json.dumps(effects)
            self.save()

    def __str__(self):
        return f"{self.enemy_type} ({self.name})"

    def get_hp(self):
        return self.base_hp * self.level

    def get_cp(self):
        return self.base_cp * self.level

    def get_dmg(self):
        if self.weakened:
            return self.base_dmg * self.level * WEAKENED_DAMAGE_MULTIPLIER
        else:
            return self.base_dmg * self.level

    def save(self, *args, **kwargs):
        self.base_hp = self.get_hp()
        self.base_cp = self.get_cp()
        self.base_dmg = self.get_dmg()
        super().save(*args, **kwargs)

    def weaken(self):
        self.weakened = True

    def unweaken(self):
        self.weakened = False


class Goblin(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Goblin"
        kwargs["base_hp"] = GOBLIN_HP
        kwargs["base_dmg"] = GOBLIN_DMG
        kwargs["base_cp"] = GOBLIN_CP
        kwargs["exp_reward"] = GOBLIN_EXP
        super().__init__(*args, **kwargs)


class Skeleton(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Skeleton"
        kwargs["base_hp"] = SKELETON_HP
        kwargs["base_dmg"] = SKELETON_DMG
        kwargs["base_cp"] = SKELETON_CP
        kwargs["exp_reward"] = SKELETON_EXP
        super().__init__(*args, **kwargs)


class Shadow(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Shadow"
        kwargs["base_hp"] = SHADOW_HP
        kwargs["base_dmg"] = SHADOW_DMG
        kwargs["base_cp"] = SHADOW_CP
        kwargs["exp_reward"] = SHADOW_EXP
        super().__init__(*args, **kwargs)


class Cobalt(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Cobalt"
        kwargs["base_hp"] = COBALT_HP
        kwargs["base_dmg"] = COBALT_DMG
        kwargs["base_cp"] = COBALT_CP
        kwargs["exp_reward"] = COBALT_EXP
        super().__init__(*args, **kwargs)


class Wolf(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Wolf"
        kwargs["base_hp"] = WOLF_HP
        kwargs["base_dmg"] = WOLF_DMG
        kwargs["base_cp"] = WOLF_CP
        kwargs["exp_reward"] = WOLF_EXP
        super().__init__(*args, **kwargs)


class Orc(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Orc"
        kwargs["base_hp"] = ORC_HP
        kwargs["base_dmg"] = ORC_DMG
        kwargs["base_cp"] = ORC_CP
        kwargs["exp_reward"] = ORC_EXP
        super().__init__(*args, **kwargs)


class Golem(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Golem"
        kwargs["base_hp"] = GOLEM_HP
        kwargs["base_dmg"] = GOLEM_DMG
        kwargs["base_cp"] = GOLEM_CP
        kwargs["exp_reward"] = GOLEM_EXP
        super().__init__(*args, **kwargs)


class Cerberus(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Cerberus"
        kwargs["base_hp"] = CERBERUS_HP
        kwargs["base_dmg"] = CERBERUS_DMG
        kwargs["base_cp"] = CERBERUS_CP
        kwargs["exp_reward"] = CERBERUS_EXP
        super().__init__(*args, **kwargs)


class Hydra(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Hydra"
        kwargs["base_hp"] = HYDRA_HP
        kwargs["base_dmg"] = HYDRA_DMG
        kwargs["base_cp"] = HYDRA_CP
        kwargs["exp_reward"] = HYDRA_EXP
        super().__init__(*args, **kwargs)


class Dragon(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Dragon"
        kwargs["base_hp"] = DRAGON_HP
        kwargs["base_dmg"] = DRAGON_DMG
        kwargs["base_cp"] = DRAGON_CP
        kwargs["exp_reward"] = DRAGON_EXP
        super().__init__(*args, **kwargs)


class BossFairy(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Fairy"
        kwargs["base_hp"] = BOSS_FAIRY_HP
        kwargs["base_dmg"] = BOSS_FAIRY_DMG
        kwargs["base_cp"] = BOSS_FAIRY_CP
        kwargs["exp_reward"] = BOSS_FAIRY_EXP
        super().__init__(*args, **kwargs)


class BossBear(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Bear"
        kwargs["base_hp"] = BOSS_BEAR_HP
        kwargs["base_dmg"] = BOSS_BEAR_DMG
        kwargs["base_cp"] = BOSS_BEAR_CP
        kwargs["exp_reward"] = BOSS_BEAR_EXP
        super().__init__(*args, **kwargs)


class BossPhoenix(EnemyModel):
    def __init__(self, *args, **kwargs):
        kwargs["enemy_type"] = "Phoenix"
        kwargs["base_hp"] = BOSS_PHOENIX_HP
        kwargs["base_dmg"] = BOSS_PHOENIX_DMG
        kwargs["base_cp"] = BOSS_PHOENIX_CP
        kwargs["exp_reward"] = BOSS_PHOENIX_EXP
        super().__init__(*args, **kwargs)
