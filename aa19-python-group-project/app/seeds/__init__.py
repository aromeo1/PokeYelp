from flask.cli import AppGroup
from .users import seed_users, undo_users
from .pokemon import seed_pokemon, undo_pokemon
from .reviews import seed_reviews, undo_reviews
from .lists import seed_lists, undo_lists
from .images import seed_images, undo_images

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')

# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will  truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_images()
        undo_lists()
        undo_reviews()
        undo_pokemon()
        undo_users()
    
    # Seed in proper order to handle dependencies
    users = seed_users()
    pokemon = seed_pokemon()
    reviews = seed_reviews()
    lists = seed_lists()
    images = seed_images()
    
    print("✅ All seeds completed successfully!")


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_images()
    undo_lists()
    undo_reviews()
    undo_pokemon()
    undo_users()
    print("✅ All seeds undone successfully!")
