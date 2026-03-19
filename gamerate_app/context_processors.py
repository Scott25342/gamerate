from .models import VideoGame

def all_game_titles(request):
    titles = VideoGame.objects.values_list('title', flat=True)
    return {'all_game_titles': titles}