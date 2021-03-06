# Generated by Django 3.2.8 on 2021-11-01 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('war_api', '0003_alter_player_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='deck',
        ),
        migrations.RemoveField(
            model_name='player',
            name='id',
        ),
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='player',
            name='wins',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('game_state', models.JSONField()),
                ('game_finished', models.BooleanField(default=False)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='war_api.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='war_api.player')),
            ],
        ),
        migrations.AddConstraint(
            model_name='game',
            constraint=models.UniqueConstraint(fields=('player1', 'player2'), name='unique_game'),
        ),
    ]
