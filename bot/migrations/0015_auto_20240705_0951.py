# Generated by Django 3.2.25 on 2024-07-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_bossfairy'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='skills',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='enemy',
            name='skills',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]