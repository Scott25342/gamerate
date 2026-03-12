from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game_library/', views.game_library, name='game_library'),
    path('game_detail/<int:game_id>/', views.game_detail, name='game_detail'),

    path("profile/", views.profile_page, name="profile"),
    path("delete_review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review")
]