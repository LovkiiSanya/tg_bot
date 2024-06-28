from django.contrib import admin
from .models import Character
from .enemies import Enemy

admin.site.register(Enemy)
admin.site.register(Character)

