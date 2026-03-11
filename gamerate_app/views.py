from django.shortcuts import render, get_object_or_404
from .models import VideoGame

# Create your views here.
def home(request):
    return render(request, 'home.html')

def game_detail(request, game_id):
    game = get_object_or_404(VideoGame, pk=game_id)
    return render(request, 'game_detail.html', {'game': game})

def game_library(request):
    games = VideoGame.objects.all()
    return render(request, 'game_library.html', {'games': games})