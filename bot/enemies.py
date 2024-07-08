import json

from django.db import models


class Enemy(models.Model):
    name = models.CharField(max_length=50)
    base_hp = models.IntegerField(default=100)
    base_cp = models.IntegerField(default=10)
    base_dmg = models.IntegerField(default=10)
    level = models.IntegerField(default=1)
    enemy_type = models.CharField(max_length=50, default='Generic')
    exp_reward = models.IntegerField(default=50)
    weakened = models.BooleanField(default=False)
    skills = models.JSONField(default=dict, blank=True)
    effects = models.CharField(max_length=255, null=True, blank=True)
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

    def __str__(self):
        return f"{self.enemy_type} ({self.name})"

    def get_hp(self):
        return self.base_hp * self.level

    def get_cp(self):
        return self.base_cp * self.level

    def get_dmg(self):
        if self.weakened:
            return self.base_dmg * self.level * 0.9
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


class Goblin(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Goblin'
        kwargs['base_hp'] = 50
        kwargs['base_dmg'] = 5
        kwargs['base_cp'] = 0
        kwargs['exp_reward'] = 50
        super().__init__(*args, **kwargs)


class Skeleton(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Skeleton'
        kwargs['base_hp'] = 100
        kwargs['base_dmg'] = 25
        kwargs['base_cp'] = 10
        kwargs['exp_reward'] = 100
        super().__init__(*args, **kwargs)


class Shadow(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Shadow'
        kwargs['base_hp'] = 80
        kwargs['base_dmg'] = 30
        kwargs['base_cp'] = 15
        kwargs['exp_reward'] = 120
        super().__init__(*args, **kwargs)


class Cobalt(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Cobalt'
        kwargs['base_hp'] = 80
        kwargs['base_dmg'] = 30
        kwargs['base_cp'] = 15
        kwargs['exp_reward'] = 120
        super().__init__(*args, **kwargs)


class Wolf(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Wolf'
        kwargs['base_hp'] = 10
        kwargs['base_dmg'] = 20
        kwargs['base_cp'] = 5
        kwargs['exp_reward'] = 100
        super().__init__(*args, **kwargs)


class Orc(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Orc'
        kwargs['base_hp'] = 15
        kwargs['base_dmg'] = 25
        kwargs['base_cp'] = 15
        kwargs['exp_reward'] = 200
        super().__init__(*args, **kwargs)


class Golem(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Golem'
        kwargs['base_hp'] = 40
        kwargs['base_dmg'] = 20
        kwargs['base_cp'] = 7
        kwargs['exp_reward'] = 2500
        super().__init__(*args, **kwargs)


class Cerberus(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Cerberus'
        kwargs['base_hp'] = 100
        kwargs['base_dmg'] = 20
        kwargs['base_cp'] = 5
        kwargs['exp_reward'] = 100
        super().__init__(*args, **kwargs)


class Hydra(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Hydra'
        kwargs['base_hp'] = 100
        kwargs['base_dmg'] = 20
        kwargs['base_cp'] = 5
        kwargs['exp_reward'] = 100
        super().__init__(*args, **kwargs)


class Dragon(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Dragon'
        kwargs['base_hp'] = 1000
        kwargs['base_dmg'] = 100
        kwargs['base_cp'] = 250
        kwargs['exp_reward'] = 500
        super().__init__(*args, **kwargs)


class BossFairy(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Fairy'
        kwargs['base_hp'] = 800
        kwargs['base_dmg'] = 100
        kwargs['base_cp'] = 25
        kwargs['exp_reward'] = 1000
        super().__init__(*args, **kwargs)


class BossBear(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Bear'
        kwargs['base_hp'] = 80
        kwargs['base_dmg'] = 100
        kwargs['base_cp'] = 25
        kwargs['exp_reward'] = 5000
        super().__init__(*args, **kwargs)


class BossPhoenix(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Phoenix'
        kwargs['base_hp'] = 800
        kwargs['base_dmg'] = 100
        kwargs['base_cp'] = 25
        kwargs['exp_reward'] = 1000
        super().__init__(*args, **kwargs)
