import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from games.models import Game, Genre, Platform, Developer, Publisher


def unique_csv_values(field, values):
    """
    Helper function to find the unique values in a csv field that contains
    multiple values.
    
    @param field: csv field to search for values
    @param values: list of unique values already found. Will be updated with the
    unique values found by this method
    """
    vals = field.split(',')
    for val in vals:
        if val == '': continue
        if val not in values: values.append(val)


def import_category(category, values):
    """
    Helper function to import values into the provided category Model.
    
    @param model: the Django Model that the values are being imported to.
    @param values: the values being imported.
    """
    for val in values:
        c = category.objects.create(name=val)
        c.save()


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Reads through the csv file and collates the unique values for genres,
        # platforms, developers, and plublishers.
        genres = []
        platforms = []
        developers = []
        publishers = []
        games = []
        with open("planning/games.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['genres'] not in genres: genres.append(row['genres'])
                unique_csv_values(row['platforms'], platforms)
                unique_csv_values(row['developer'], developers)
                unique_csv_values(row['publisher'], publishers)
                
                # Convert date to datetime.date object
                release_date = ''
                if row['releaseDate'] != '': release_date = datetime.strptime(row['releaseDate'], '%Y-%m-%d').date()
                # Appends to a list of games with each game's relevant data
                games.append((row['title'], release_date, row['rating'],
                            row['genres'], row['description'], row['platforms'],
                            row['developer'], row['publisher']))
        
        # Insert all unique values into the database tables.
        import_category(Genre, genres)
        import_category(Platform, platforms)
        import_category(Developer, developers)
        import_category(Publisher, publishers)
        
        # Insert all games into the Game table.
        for game in games:
            genre = Genre.objects.get(name=game[3])
            g = Game.objects.create(title=game[0], release_date=game[1],
                                    rating=game[2], genre=genre,
                                    description=game[4])
            g.save()
            for plat in game[5].split(','):
                if plat == '': continue
                platform = Platform.objects.get(name=plat)
                g.platforms.add(platform)
            for dev in game[6].split(','):
                if dev == '': continue
                developer = Developer.objects.get(name=dev)
                g.developers.add(developer)
            for pub in game[7].split(','):
                if pub == '': continue
                publisher = Publisher.objects.get(name=pub)
                g.publishers.add(publisher)
