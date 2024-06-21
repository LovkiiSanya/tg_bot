# Generated by Django 3.2.12 on 2024-06-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20240625_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='level',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='character',
            name='role',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
