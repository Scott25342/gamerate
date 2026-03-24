from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import VideoGame, Review
from django.db.models import Avg, Count
from .forms import UserRegistrationForm, UserLoginForm, ReviewForm



# Create your views here.
def home(request):
    top_game = VideoGame.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating').first()  
    most_popular = VideoGame.objects.annotate(num_reviews=Count('review'),avg_rating=Avg('review__rating')).order_by("-num_reviews").first()
        
    context_dict = {
        'best_rated_game': top_game,
        'most_popular_game': most_popular,
    }
    return render(request, 'home.html', context=context_dict)

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(VideoGame, pk=game_id)
    reviews = Review.objects.filter(game=game).order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
            return redirect('game_detail', game_id=game_id)
    else:
        form = ReviewForm

    return render(request, 'game_detail.html', {'game': game, 'reviews': reviews, 'form': form, 'avg_rating': avg_rating})

def game_library(request):
    games = VideoGame.objects.all()
    genres = VideoGame.objects.values_list('genre', flat=True).distinct()
    genre_filter = request.GET.get('genre')

    if genre_filter:
        games = games.filter(genre=genre_filter)

    context = {
        'games': games,
        'genres': genres
    }
    return render(request, 'game_library.html', context)


def register(request):
    registered = False

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            registered = True
            form = UserRegistrationForm()
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form, "registered": registered})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = UserLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(reverse("home"))

        form.add_error(None, "Invalid username or password.")

    return render(request, "login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("home"))


@login_required
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


@login_required
def delete_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        review.delete()

    return redirect("profile")


@login_required
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

@staff_member_required
def edit_game(request, game_id):
    game = get_object_or_404(VideoGame, id=game_id)

    if request.method == "POST":
        game.title = request.POST.get("title")
        game.genre = request.POST.get("genre")
        game.rating = request.POST.get("rating")
        game.release_year = request.POST.get("release_year")
        game.developer = request.POST.get("developer")
        game.description = request.POST.get("description")
        game.image = request.POST.get("image")
        game.save()
        return redirect("game_detail", game_id=game.id)

    return render(request, "edit_game.html", {"game": game})


@staff_member_required
def delete_game(request, game_id):
    game = get_object_or_404(VideoGame, id=game_id)

    if request.method == "POST":
        game.delete()
        return redirect("game_library")

    return render(request, "delete_game.html", {"game": game})

@staff_member_required
def add_game(request):
    if request.method == "POST":
        title = request.POST.get("title")
        genre = request.POST.get("genre")
        rating = request.POST.get("rating") or None
        release_year = request.POST.get("release_year")
        developer = request.POST.get("developer")
        description = request.POST.get("description")
        image = request.POST.get("image")

        game = VideoGame.objects.create(
            title=title,
            genre=genre,
            rating=rating,
            release_year=release_year,
            developer=developer,
            description=description,
            image=image
        )
        return redirect("game_detail", game_id=game.id)

    return render(request, "add_game.html")

def game_search(request):
    query = request.GET.get('query', '').strip()

    if query:
        game = VideoGame.objects.filter(title__iexact=query).first()

        if game:
            return redirect('game_detail', game_id=game.id)
        
    return redirect('home')