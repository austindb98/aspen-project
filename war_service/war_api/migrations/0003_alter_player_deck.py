# Generated by Django 3.2.8 on 2021-10-30 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('war_api', '0002_player_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='deck',
            field=models.JSONField(default=dict),
        ),
    ]
