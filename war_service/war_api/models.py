from email.policy import default
from tkinter import CASCADE
from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    wins = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)


class Game(models.Model):
    player1 = models.ForeignKey(
        Player, related_name="player1", on_delete=models.CASCADE
    )
    player2 = models.ForeignKey(
        Player, related_name="player2", on_delete=models.CASCADE
    )
    game_state = models.JSONField()
    game_finished = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["player1", "player2"], name="unique_game")
        ]
