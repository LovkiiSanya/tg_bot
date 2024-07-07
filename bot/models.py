import json
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from bot.management.commands.game_dice import apply_random_effect
import logging


class Character(models.Model):
    user_id = models.IntegerField(unique=True, default=0)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    hp = models.IntegerField(default=100)
    mp = models.IntegerField(default=50)
    cp = models.IntegerField(default=10)
    dmg = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    effects = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=50, default='location_selection')
    temp_stats = JSONField(default=dict)
    regenerate = models.BooleanField(default=False)
    regenerate_amount = models.IntegerField(default=0)
    lose_health = models.BooleanField(default=False)
    lose_health_amount = models.IntegerField(default=0)
    in_battle = models.BooleanField(default=False)
    completed_locations = models.IntegerField(default=0)
    completed_forest_levels = models.IntegerField(default=0)
    completed_catacombs_levels = models.IntegerField(default=0)
    completed_magma_levels = models.IntegerField(default=0)
    current_forest_level = models.IntegerField(default=1)
    current_catacombs_level = models.IntegerField(default=1)
    current_magma_level = models.IntegerField(default=1)
    dodge_modifier = models.IntegerField(default=0)
    crit_chance_modifier = models.FloatField(default=0.0)
    skills = models.JSONField(default=dict, blank=True)
    skill_effects = models.TextField(default='{}')

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
            del effects[effect_name]
            self.skill_effects = json.dumps(effects)
            self.save()

    def level_up(self):
        self.level += 1
        self.hp += 10
        self.mp += 5
        self.cp += 5
        self.dmg += 2
        self.save()

    def add_experience(self, exp_gained):
        self.exp += exp_gained
        while self.exp >= 100 * self.level:
            self.exp -= 100 * self.level
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
        cls_dodge_map = {
            'Mage': 1.5,
            'Tank': 2,
            'Duelist': 2.5
        }
        return self.level * cls_dodge_map.get(self.role, 0)

    def calculate_crit(self):
        cls_crit_map = {
            'Mage': 5,
            'Tank': 2,
            'Duelist': 3
        }
        return self.dmg * cls_crit_map.get(self.role, 0)

    def calculate_crit_chance(self):
        cls_crit_chance_map = {
            'Mage': 0.1,
            'Tank': 0.2,
            'Duelist': 0.3
        }
        return self.dmg * cls_crit_chance_map.get(self.role, 0)

    def save(self, *args, **kwargs):
        self._dodge = self.calculate_dodge()
        self._crit_chance = self.calculate_crit_chance()
        super().save(*args, **kwargs)

    # def apply_random_effect(self):
    #     apply_random_effect(self)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return f"Character(dmg={self.dmg}, dodge={self.dodge}%, crit={self.crit}, crit_chance={self.crit_chance}%, exp={self.exp}, level={self.level})"
