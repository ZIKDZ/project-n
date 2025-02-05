from django import forms
from .models import Player, Rank, Game
from django.core.exceptions import ValidationError 

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'game', 'rank', 'in_game_username', 'discord_username', 'email']

    rank = forms.ModelChoiceField(
        queryset=Rank.objects.none(),  # Initially empty, will be populated via AJAX
        widget=forms.Select(attrs={"id": "rank-dropdown"})  # Add ID for JavaScript
    )

    def __init__(self, *args, **kwargs):
        game_id = kwargs.get('initial', {}).get('game_id', None)
        super(PlayerForm, self).__init__(*args, **kwargs)

        if game_id:
            # Populate the rank queryset based on the selected game_id
            self.fields['rank'].queryset = Rank.objects.filter(game_id=game_id)

        # Ensure that the game field has the correct ID for JavaScript
        self.fields['game'].widget.attrs['id'] = 'game-dropdown'
    
    # Errors Logging

    def clean_username(self):
            username = self.cleaned_data.get('username')
            if Player.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")
            return username 
    def clean_in_game_username(self):
        in_game_username = self.cleaned_data.get('in_game_username')
        if Player.objects.filter(in_game_username=in_game_username).exists():
            raise ValidationError("This in-game username is already taken.")
        return in_game_username 
    def clean_discord_username(self):
        discord_username = self.cleaned_data.get('discord_username')
        if Player.objects.filter(discord_username=discord_username).exists():
            raise ValidationError("This Discord username is already in use.")
        return discord_username 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Player.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email