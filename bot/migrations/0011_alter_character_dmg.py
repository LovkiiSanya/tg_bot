# Generated by Django 3.2.25 on 2024-06-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_auto_20240626_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='dmg',
            field=models.IntegerField(default=0),
        ),
    ]
