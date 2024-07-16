from django.contrib import admin
from .models import Character
from .enemies import EnemyModel

admin.site.register(EnemyModel)
admin.site.register(Character)
