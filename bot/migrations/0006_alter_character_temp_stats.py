# Generated by Django 3.2.25 on 2024-07-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_character_temp_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='temp_stats',
            field=models.JSONField(default=dict),
        ),
    ]
