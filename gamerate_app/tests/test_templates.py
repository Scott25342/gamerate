from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from gamerate_app.models import VideoGame, Review

class TemplateTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.game = VideoGame.objects.create(
            title="Test Game",
            genre="RPG",
            rating=9,
            release_year=2020,
            developer="Test Dev"
        )

        self.review = Review.objects.create(
            user=self.user,
            game=self.game,
            rating=8,
            review_text="Great game"
        )

    def test_home_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_displays_game(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.game.title)

    def test_game_detail_template_used(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('game_detail', args=[self.game.id]))
        self.assertTemplateUsed(response, 'game_detail.html')

    def test_game_detail_displays_review(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('game_detail', args=[self.game.id]))
        self.assertContains(response, self.review.review_text)

    def test_game_library_template_used(self):
        response = self.client.get(reverse('game_library'))
        self.assertTemplateUsed(response, 'game_library.html')

    def test_game_library_lists_games(self):
        response = self.client.get(reverse('game_library'))
        self.assertContains(response, self.game.title)

    def test_profile_template_used(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_displays_user_reviews(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('profile'))
        self.assertContains(response, self.review.review_text)

    def test_search_redirects(self):
        response = self.client.get(reverse('game_search') + '?query=Test Game')
        self.assertEqual(response.status_code, 302)