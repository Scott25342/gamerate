from django.core.management.base import BaseCommand
import requests
from gamerate_app.models import VideoGame

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        url = "https://www.freetogame.com/api/games"
        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"API request failed: {response.status_code}"))
            return
        
        games = response.json()
        imported = 0

        for g in games:
            release_year = None
            if g.get("release_date"):
                try:
                    release_year = int(g["release_date"].split("-")[0])
                except ValueError:
                    pass

            VideoGame.objects.update_or_create(
                title=g["title"],
                defaults={
                    "genre": g.get("genre", ""),
                    "release_year": release_year,
                    "developer": g.get("developer", ""),
                    "description": g.get("short_description", ""),
                    "image": g.get("thumbnail", ""),
                }
            )
            imported += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {imported} games successfully!"))