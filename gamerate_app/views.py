from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import VideoGame, Review



# Create your views here.
def home(request):
    return render(request, 'home.html')

def game_detail(request, game_id):
    game = get_object_or_404(VideoGame, pk=game_id)
    return render(request, 'game_detail.html', {'game': game})

def game_library(request):
    games = VideoGame.objects.all()
    return render(request, 'game_library.html', {'games': games})


def profile_page(request):

    reviews = []
    top_ratings = []

    if request.user.is_authenticated:
        reviews = request.user.reviews.all()
        top_ratings = reviews.order_by("-rating")[:5]

    context = {
        "reviews": reviews,
        "top_ratings": top_ratings
    }

    return render(request, "profile.html", context)

def delete_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        review.delete()

    return redirect("profile")

def edit_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("profile")

    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.review_text = request.POST.get("review_text")
        review.save()
        return redirect("profile")

    return render(request, "edit_review.html", {"review": review})