from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count

from gamerate_app.models import VideoGame, Review
from gamerate_app.forms import ReviewForm

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.game1 = VideoGame.objects.create(title="Game1", genre="RPG", rating=8, release_year=2020, developer="Dev1")
        self.game2 = VideoGame.objects.create(title="Game2", genre="Action", rating=5, release_year=2021, developer="Dev2")

        user = User.objects.create_user(username="testuser", password="password123")
        Review.objects.create(user=user, game=self.game1, rating=10, review_text="Great game")

    def test_home_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.context['best_rated_game'], self.game1)
        self.assertEqual(response.context['most_popular_game'], self.game1)

class GameDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.game = VideoGame.objects.create(title="Game1", genre="RPG", rating=9, release_year=2020, developer="Dev1")

    def test_game_detail_requires_login(self):
        url = reverse('game_detail', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_game_detail_get(self):
        self.client.login(username="testuser", password="password123")
        url = reverse('game_detail', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_detail.html')
        self.assertIsInstance(response.context['form'], type(ReviewForm))
        self.assertEqual(response.context['game'], self.game)

    def test_game_detail_post_valid_review(self):
        self.client.login(username="testuser", password="password123")
        url = reverse('game_detail', args=[self.game.id])
        response = self.client.post(url, {'rating': 8, 'review_text': "Good game"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.game, self.game)

class GameLibraryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.game1 = VideoGame.objects.create(title="Game1", genre="RPG", rating=8, release_year=2020, developer="Dev1")
        self.game2 = VideoGame.objects.create(title="Game2", genre="Action", rating=5, release_year=2021, developer="Dev2")

    def test_game_library_all_games(self):
        response = self.client.get(reverse('game_library'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_library.html')
        self.assertEqual(set(response.context['games']), {self.game1, self.game2})

    def test_game_library_filter_genre(self):
        response = self.client.get(reverse('game_library') + '?genre=RPG')
        self.assertEqual(list(response.context['games']), [self.game1])

class ProfilePageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.game = VideoGame.objects.create(title="Game1", genre="RPG", rating=8, release_year=2020, developer="Dev1")
        Review.objects.create(user=self.user, game=self.game, rating=10, review_text="Great game")

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_shows_reviews(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(list(response.context['reviews']), list(self.user.reviews.all()))
        self.assertEqual(list(response.context['top_ratings']), list(self.user.reviews.order_by('-rating')[:5]))

class GameSearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = VideoGame.objects.create(title="Game1", genre="RPG", rating=8, release_year=2020, developer="Dev1")

    def test_game_search_redirect_found(self):
        response = self.client.get(reverse('game_search') + '?query=Game1')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('game_detail', args=[self.game.id]), response.url)

    def test_game_search_redirect_not_found(self):
        response = self.client.get(reverse('game_search') + '?query=Nonexistent')
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('home'), response.url)