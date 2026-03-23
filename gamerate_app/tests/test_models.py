from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from gamerate_app.models import VideoGame, Review

class VideoGameModelTests(TestCase):
    def setUp(self):
        self.game = VideoGame.objects.create(
            title="Batman: Arkham Asylum",
            genre="Action Adventure",
            rating=9.5,
            release_year=2009,
            developer="RockSteady",
            description="control Batman as he fights his way through a riotous, isolated asylum filled with his most dangerous enemies, " \
            "combining fluid combat, stealth gameplay, and detective work in a polished, gothic atmosphere.",
            image="https://exampleUrl.com/exampleImage.jpg"
        )

    def test_video_game_creation(self):
        self.assertEqual(self.game.title, "Batman: Arkham Asylum")
        self.assertEqual(self.game.genre, "Action Adventure")
        self.assertEqual(self.game.rating, 9.5)

    def test_video_game_str(self):
        self.assertEqual(str(self.game), "Batman: Arkham Asylum")

    def test_title_is_unique(self):
        with self.assertRaises(IntegrityError):
            VideoGame.objects.create(
                title="Batman: Arkham Asylum",
                genre="Action Adventure",
                release_year=2009,
                developer="RockSteady"
            )
    
class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.game = VideoGame.objects.create(
            title="Batman: Arkham Asylum",
            genre="Action Adventure",
            release_year=2009,
            developer="RockSteady"
        )

        self.review = Review.objects.create(
            user=self.user,
            game=self.game,
            rating=8,
            review_text="Great game"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.user.username, "testuser")
        self.assertEqual(self.review.game.title, "Batman: Arkham Asylum")
        self.assertEqual(self.review.rating, 8)

    def test_review_str(self):
        expected_str = f"{self.user.username} - {self.game.title}"
        self.assertEqual(str(self.review), expected_str)

    def test_rating_validation_valid(self):
        review = Review(
            user=self.user,
            game=self.game,
            rating=10,
            review_text="Perfect game"
        )
        review.full_clean()

    def test_rating_validation_invalid_low(self):
        review = Review(
            user=self.user,
            game=self.game,
            rating=0,
            review_text="Too low"
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_validation_invalid_high(self):
        review = Review(
            user=self.user,
            game=self.game,
            rating=11,
            review_text="Too high"
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_cascade_delete_user(self):
        self.user.delete()
        self.assertEqual(Review.objects.count(), 0)

    def test_review_cascade_delete_game(self):
        self.game.delete()
        self.assertEqual(Review.objects.count(), 0)