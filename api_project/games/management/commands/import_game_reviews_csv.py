import csv
import secrets
from datetime import datetime
from django.core.management.base import BaseCommand
from games.models import Review, User, Game


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        users = []
        reviews = []
        with open("planning/games_reviews.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 1
            for row in reader:
                # Exclude reviews with no publish date or score
                if row['date'] == '' or row['score'] == '': continue
                
                # Add unique users (author or publication name)
                if row['author'] != '': user = row['author']
                else: user = row['publicationName']
                if user not in users: users.append(user)
                
                publish_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                reviews.append((user, row['title'], publish_date,
                                int(float(row['score'])), row['quote']))
                count += 1
                if count > 125000:
                    break

        # Insert users into the database
        User.objects.bulk_create([
            User(
                username=user,
                password=secrets.token_urlsafe(32),
                is_active=True,
            ) for user in users
        ])

        # Insert reviews into the database
        Review.objects.bulk_create([
            Review(user=User.objects.get(username=review[0]),
                   game=Game.objects.get(title=review[1]),
                   date=review[2],
                   score=review[3],
                   content=review[4]
                ) for review in reviews
        ])
