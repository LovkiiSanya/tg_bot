import json
from django.db import models

# Constants
MAX_NICKNAME_LENGTH = 50
MAX_ROLE_LENGTH = 50
DEFAULT_HP = 100
DEFAULT_MP = 10
DEFAULT_CP = 10
DEFAULT_DMG = 10
DEFAULT_EXP = 0
DEFAULT_LEVEL = 1
DEFAULT_EFFECTS = ""
DEFAULT_STATE = "Idle"
DEFAULT_REGENERATE = False
DEFAULT_REGENERATE_AMOUNT = 0
DEFAULT_LOSE_HEALTH = False
DEFAULT_LOSE_HEALTH_AMOUNT = 0
DEFAULT_IN_BATTLE = False
DEFAULT_COMPLETED_LOCATIONS = 0
DEFAULT_COMPLETED_FOREST_LEVELS = 0
DEFAULT_COMPLETED_CATACOMBS_LEVELS = 0
DEFAULT_COMPLETED_MAGMA_LEVELS = 1
DEFAULT_CURRENT_FOREST_LEVEL = 1
DEFAULT_CURRENT_CATACOMBS_LEVEL = 1
DEFAULT_CURRENT_MAGMA_LEVEL = 1
DEFAULT_DODGE_MODIFIER = 0
DEFAULT_CRIT_CHANCE_MODIFIER = 0.0
LEVEL_UP_HP_INCREMENT = 20
LEVEL_UP_MP_INCREMENT = 5
LEVEL_UP_CP_INCREMENT = 5
LEVEL_UP_DMG_INCREMENT = 5
EXP_PER_LEVEL = 100
DODGE_MAP = {'Mage': 1.5,
             'Tank': 2,
             'Duelist': 2.5}
CRIT_MAP = {'Mage': 5,
            'Tank': 2,
            'Duelist': 3}
CRIT_CHANCE_MAP = {'Mage': 0.1,
                   'Tank': 0.2,
                   'Duelist': 0.3}


# Updated Models
class Character(models.Model):
    user_id = models.IntegerField(unique=True)
    nickname = models.CharField(max_length=MAX_NICKNAME_LENGTH, null=True, blank=True)
    role = models.CharField(max_length=MAX_ROLE_LENGTH, null=True, blank=True)
    hp = models.IntegerField(default=DEFAULT_HP)
    mp = models.IntegerField(default=DEFAULT_MP)
    cp = models.IntegerField(default=DEFAULT_CP)
    dmg = models.IntegerField(default=DEFAULT_DMG)
    exp = models.IntegerField(default=DEFAULT_EXP)
    level = models.IntegerField(default=DEFAULT_LEVEL)
    effects = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=MAX_ROLE_LENGTH, default=DEFAULT_STATE)
    temp_stats = models.JSONField(default=dict)
    regenerate = models.BooleanField(default=DEFAULT_REGENERATE)
    regenerate_amount = models.IntegerField(default=DEFAULT_REGENERATE_AMOUNT)
    lose_health = models.BooleanField(default=DEFAULT_LOSE_HEALTH)
    lose_health_amount = models.IntegerField(default=DEFAULT_LOSE_HEALTH_AMOUNT)
    in_battle = models.BooleanField(default=DEFAULT_IN_BATTLE)
    completed_locations = models.IntegerField(default=DEFAULT_COMPLETED_LOCATIONS)
    completed_forest_levels = models.IntegerField(default=DEFAULT_COMPLETED_FOREST_LEVELS)
    completed_catacombs_levels = models.IntegerField(default=DEFAULT_COMPLETED_CATACOMBS_LEVELS)
    completed_magma_levels = models.IntegerField(default=DEFAULT_COMPLETED_MAGMA_LEVELS)
    current_forest_level = models.IntegerField(default=DEFAULT_CURRENT_FOREST_LEVEL)
    current_catacombs_level = models.IntegerField(default=DEFAULT_CURRENT_CATACOMBS_LEVEL)
    current_magma_level = models.IntegerField(default=DEFAULT_CURRENT_MAGMA_LEVEL)
    dodge_modifier = models.IntegerField(default=DEFAULT_DODGE_MODIFIER)
    crit_chance_modifier = models.FloatField(default=DEFAULT_CRIT_CHANCE_MODIFIER)
    skills = models.JSONField(default=dict, blank=True)
    skill_effects = models.TextField(default="{}")

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

    def level_up(self):
        self.level += 1
        self.hp += LEVEL_UP_HP_INCREMENT
        self.mp += LEVEL_UP_MP_INCREMENT
        self.cp += LEVEL_UP_CP_INCREMENT
        self.dmg += LEVEL_UP_DMG_INCREMENT
        self.save()

    def add_experience(self, exp_gained):
        self.exp += exp_gained
        while self.exp >= EXP_PER_LEVEL * self.level:
            self.exp -= EXP_PER_LEVEL * self.level
            self.level_up()
        self.save()

    @property
    def dodge(self):
        return self.calculate_dodge() + self.dodge_modifier

    @property
    def crit(self):
        return self.calculate_crit()

    @property
    def crit_chance(self):
        return self.calculate_crit_chance() + self.crit_chance_modifier

    def calculate_dodge(self):
        return self.level * DODGE_MAP.get(self.role, 0)

    def calculate_crit(self):
        return self.dmg * CRIT_MAP.get(self.role, 0)

    def calculate_crit_chance(self):
        return self.dmg * CRIT_CHANCE_MAP.get(self.role, 0)

    def save(self, *args, **kwargs):
        self._dodge = self.calculate_dodge()
        self._crit_chance = self.calculate_crit_chance()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return "Character(dmg={}, dodge={}%, crit={}, crit_chance={}%, exp={}, level={})".format(
            self.dmg, self.dodge, self.crit, self.crit_chance, self.exp, self.level
        )


