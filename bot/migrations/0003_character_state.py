# Generated by Django 3.2.25 on 2024-06-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20240628_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='state',
            field=models.CharField(default='start', max_length=50),
        ),
    ]