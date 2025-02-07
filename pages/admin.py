from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from .models import Game, Rank, Player, Team

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("rank_name", "game")

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("username", "game", "rank", "application_status", "created_at")
    list_filter = ("game", "application_status")
    search_fields = ("username", "discord_username", "email")
    ordering = ("-created_at",)
    list_editable = ("application_status",)

    # Set the custom template for the add page
    change_form_template = "admin/NBLEsport/player/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_ranks/', self.get_ranks, name='get_ranks'),
        ]
        return custom_urls + urls

    def get_ranks(self, request):
        """Handle the Ajax request to fetch ranks for a selected game."""
        game_id = request.GET.get('game_id')
        ranks = Rank.objects.filter(game_id=game_id).values('id', 'rank_name')
        return JsonResponse(list(ranks), safe=False)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "game", "coach", "team_manager", "created_at")
    list_filter = ("game",)
    search_fields = ("name",)
    ordering = ("-created_at",)
    filter_horizontal = ("players",)  # Adds a nice UI for ManyToMany fields
