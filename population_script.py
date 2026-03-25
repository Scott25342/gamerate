import os,csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'gamerate.settings')

import django
django.setup()
from gamerate_app.models import VideoGame,Review
from django.contrib.auth.models import User

def populate():
    game_data = []
    with open("games.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['rating'] = float(row['rating']) if row['rating'] else None
            row['release_year'] = int(row['release_year']) if row['release_year'] else None
            game_data.append(row)
            game_obj, created = VideoGame.objects.update_or_create(
            title=row['title'],  
            defaults=row          
            )
            print(f"{'Created' if created else 'Updated'}: {row['title']}")
    

   #-----Test user-----
    user1,_ = User.objects.get_or_create(username="alice")
    user2,_ = User.objects.get_or_create(username="charlie")
    user3,_ = User.objects.get_or_create(username="eve")

    minecraft = VideoGame.objects.get(title="Minecraft")
    cyberpunk = VideoGame.objects.get(title="Cyberpunk 2077")
    elden_ring = VideoGame.objects.get(title="Elden Ring")

    Review.objects.create(user=user1, game=minecraft, rating=8, review_text="Fun and endless creativity!")
    Review.objects.create(user=user2, game=minecraft, rating=8, review_text="Love it!")
    Review.objects.create(user=user3, game=minecraft, rating=7, review_text="Thoroughly enjoyable game!")
    Review.objects.create(user=user1, game=cyberpunk, rating=5, review_text="It's Ok.")
    Review.objects.create(user=user2, game=cyberpunk, rating=7, review_text="Pretty decent.")
    Review.objects.create(user=user3, game=elden_ring, rating=10, review_text="Incredible game!")
    print("Database populated")

    
if __name__ == "__main__":
    populate()