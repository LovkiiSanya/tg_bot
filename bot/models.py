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
    state = models.CharField(max_length=50, default='start')
    temp_stats = JSONField(default=dict)

    def level_up(self):
        print(f"Leveling up! Current level: {self.level}, experience: {self.exp}")
        self.level += 1
        self.hp += 10  # Увеличение HP на уровень
        self.mp += 5  # Увеличение MP на уровень
        self.cp += 5  # Увеличение CP на уровень
        self.dmg += 2  # Увеличение урона на уровень
        self.save()
        print(f"New level: {self.level}, new experience threshold: {100 * self.level}")

    def add_experience(self, exp_gained):
        self.exp += exp_gained
        print(f"Adding experience: {exp_gained}, current experience: {self.exp}")
        while self.exp >= 100 * self.level:
            print(f"Experience {self.exp} >= {100 * self.level}")
            self.exp -= 100 * self.level
            self.level_up()
        self.save()
        print(f"Final experience: {self.exp}, level: {self.level}")

    @property
    def dodge(self):
        return self.calculate_dodge()

    @property
    def crit(self):
        return self.calculate_crit()

    @property
    def crit_chance(self):
        return self.calculate_crit_chance()

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

    def apply_random_effect(self):
        apply_random_effect(self)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return f"Character(dmg={self.dmg}, dodge={self.dodge}%, crit={self.crit}, crit_chance={self.crit_chance}%, exp={self.exp}, level={self.level})"
