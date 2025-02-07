from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Rank(models.Model):
    game = models.ForeignKey(Game, related_name="ranks", on_delete=models.CASCADE)
    rank_name = models.CharField(max_length=50)
    rank_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['rank_order']

    def __str__(self):
        return f"{self.rank_name} ({self.game.name})"

class Player(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    username = models.CharField(max_length=50, unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    in_game_username = models.CharField(max_length=50)
    discord_username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True)
    application_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.game.name}) - {self.application_status}"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="teams")
    players = models.ManyToManyField(Player, related_name="teams")
    coach = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name="coached_teams")
    team_manager = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name="managed_teams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.game.name})"
