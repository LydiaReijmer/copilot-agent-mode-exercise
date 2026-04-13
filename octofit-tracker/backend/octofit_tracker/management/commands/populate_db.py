from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from djongo import models



from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel = {'name': 'Team Marvel'}
        dc = {'name': 'Team DC'}
        marvel_id = db.teams.insert_one(marvel).inserted_id
        dc_id = db.teams.insert_one(dc).inserted_id

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user_email': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'cap@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'batman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Yoga', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'user_email': 'ironman@marvel.com', 'workout': 'Chest Day', 'reps': 100},
            {'user_email': 'cap@marvel.com', 'workout': 'Leg Day', 'reps': 120},
            {'user_email': 'batman@dc.com', 'workout': 'Back Day', 'reps': 110},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Core Day', 'reps': 130},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'user_email': 'ironman@marvel.com', 'points': 100},
            {'user_email': 'cap@marvel.com', 'points': 90},
            {'user_email': 'batman@dc.com', 'points': 95},
            {'user_email': 'wonderwoman@dc.com', 'points': 105},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Ensure unique index on email
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
