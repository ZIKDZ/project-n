from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Rank
from .forms import PlayerForm

def home(request):
    return render(request, "pages/home.html")

def join_us(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        # Ensure rank choices are updated based on the game_id submitted with the form
        game_id = request.POST.get('game')  # Get the selected game ID from the POST data
        if game_id:
            form.fields['rank'].queryset = Rank.objects.filter(game_id=game_id)
        
        if form.is_valid():
            form.save()
            return redirect("join_us_success")
        else:
            print("Form errors: ", form.errors)  # Print form validation errors to debug

    else:
        # Get the selected game_id from the GET request (or None if not set)
        game_id = request.GET.get('game_id', None)
        form = PlayerForm(initial={'game_id': game_id})

    return render(request, "pages/join_us/join_us.html", {"form": form})

def get_ranks(request):
    game_id = request.GET.get("game_id")
    if game_id:
        ranks = Rank.objects.filter(game_id=game_id).values("id", "rank_name")
        return JsonResponse(list(ranks), safe=False)
    return JsonResponse([], safe=False)


def join_us_success(request):
    return render(request, "pages/join_us/join_us_success.html")

