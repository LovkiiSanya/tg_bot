# Generated by Django 3.2.25 on 2024-07-03 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_enemy_weakened'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='in_battle',
            field=models.BooleanField(default=False),
        ),
    ]
