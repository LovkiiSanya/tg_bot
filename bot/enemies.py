from django.db import models


class Enemy(models.Model):
    name = models.CharField(max_length=50)
    base_hp = models.IntegerField(default=100)
    base_cp = models.IntegerField(default=10)
    base_dmg = models.IntegerField(default=10)
    level = models.IntegerField(default=1)
    enemy_type = models.CharField(max_length=50, default='Generic')

    def __str__(self):
        return f"{self.enemy_type} ({self.name})"

    def get_hp(self):
        return self.base_hp * self.level

    def get_cp(self):
        return self.base_cp * self.level

    def get_dmg(self):
        return self.base_dmg * self.level


class Goblin(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Goblin'
        kwargs['base_hp'] = 50
        kwargs['base_dmg'] = 5
        super().__init__(*args, **kwargs)


class Wolf(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Wolf'
        kwargs['base_hp'] = 100
        kwargs['base_dmg'] = 20
        super().__init__(*args, **kwargs)


class Orc(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Orc'
        kwargs['base_hp'] = 150
        kwargs['base_dmg'] = 25
        kwargs['base_cp'] = 15
        super().__init__(*args, **kwargs)


class Golem(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Golem'
        kwargs['base_hp'] = 400
        kwargs['base_dmg'] = 20
        kwargs['base_cp'] = 75
        super().__init__(*args, **kwargs)


class Dragon(Enemy):
    def __init__(self, *args, **kwargs):
        kwargs['enemy_type'] = 'Dragon'
        kwargs['base_hp'] = 1000
        kwargs['base_dmg'] = 100
        kwargs['base_cp'] = 250
        super().__init__(*args, **kwargs)
