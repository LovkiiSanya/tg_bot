# Generated by Django 3.2.25 on 2024-07-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_alter_character_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='crit_chance_modifier',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='character',
            name='dodge_modifier',
            field=models.IntegerField(default=0),
        ),
    ]
