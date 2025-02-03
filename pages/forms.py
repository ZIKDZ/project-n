from django import forms
from .models import Player, Rank, Game  # Assuming you have a Game model as well

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
