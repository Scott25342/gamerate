from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game_library/', views.game_library, name='game_library'),
    path('game_detail/<int:game_id>/', views.game_detail, name='game_detail'),
]