from django.db import models
from django.contrib.auth.models import User
from bot.management.commands.game_dice import apply_random_effect


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
        if self.role == 'Mage':
            return self.level * 1.5
        elif self.role == 'Tank':
            return self.level * 2
        elif self.role == 'Duelist':
            return self.level * 2.5
        return 0

    def calculate_crit(self):
        if self.role == 'Mage':
            return self.dmg * 5
        elif self.role == 'Tank':
            return self.dmg * 2
        elif self.role == 'Duelist':
            return self.dmg * 3

    def calculate_crit_chance(self):
        if self.role == 'Mage':
            return self.dmg * 0.1
        elif self.role == 'Tank':
            return self.dmg * 0.2
        elif self.role == 'Duelist':
            return self.dmg * 0.3

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
