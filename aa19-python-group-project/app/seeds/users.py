from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash


# Adds demo users with proper password hashing
def seed_users():
    users = [
        {"username": "Demo", "email": "demo@aa.io", "password": "password"},
        {"username": "marnie", "email": "marnie@aa.io", "password": "password"},
        {"username": "bobbie", "email": "bobbie@aa.io", "password": "password"},
        {"username": "ash", "email": "ash@aa.io", "password": "password"}
    ]
    
    created_users = {}
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data["username"]).first()
        if not existing_user:
            user = User(
                username=user_data["username"], 
                email=user_data["email"], 
                password=user_data["password"]
            )
            db.session.add(user)
            db.session.flush()
            created_users[user.username] = user
        else:
            created_users[existing_user.username] = existing_user
    
    db.session.commit()
    
    # Return the created users for reference in other seeders
    return created_users


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()
