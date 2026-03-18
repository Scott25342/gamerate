from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.game_search, name='game_search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('game_library/', views.game_library, name='game_library'),
    path('game_detail/<int:game_id>/', views.game_detail, name='game_detail'),
    path("edit_game/<int:game_id>/", views.edit_game, name="edit_game"),
    path("delete_game/<int:game_id>/", views.delete_game, name="delete_game"),
    path("add_game/", views.add_game, name="add_game"),

    path("profile/", views.profile_page, name="profile"),
    path("delete_review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review")
]