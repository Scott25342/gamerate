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
    minecraft = VideoGame.objects.get(title="Minecraft")
    Review.objects.create(user=user1, game=minecraft, rating=8, review_text="Fun and endless creativity!")
    print("Database populated")

    
if __name__ == "__main__":
    populate()