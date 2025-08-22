from app.models import db, Review, User, Pokemon, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_reviews():
    # Get actual users and pokemon from the database
    users = User.query.all()
    pokemon = Pokemon.query.all()
    
    if not users or not pokemon:
        print("Warning: No users or pokemon found. Skipping reviews seeding.")
        return {}
    
    # Create reviews with actual user and pokemon references
    review_data = [
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[0],  # Pikachu
            "rating": 5,
            "title": "Absolutely shocking experience!",
            "body": "Pikachu was incredibly energetic and friendly. The electric atmosphere was amazing! Definitely worth visiting if you're looking for a spark in your Pokemon journey.",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[1] if len(users) > 1 else users[0],  # marnie or fallback
            "pokemon": pokemon[0],  # Pikachu
            "rating": 4,
            "title": "Cute but crowded",
            "body": "Pikachu is adorable as expected, but the location was quite crowded with other trainers. Still, the experience was electrifying!",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[1] if len(pokemon) > 1 else pokemon[0],  # Charizard or fallback
            "rating": 5,
            "title": "Fire-breathing excellence!",
            "body": "Charizard was majestic and powerful. The valley location is breathtaking, and watching Charizard fly was an unforgettable experience.",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[2] if len(users) > 2 else users[0],  # bobbie or fallback
            "pokemon": pokemon[2] if len(pokemon) > 2 else pokemon[0],  # Blastoise or fallback
            "rating": 4,
            "title": "Water you waiting for?",
            "body": "Blastoise was impressive with those water cannons! The gym setting is perfect, though it can get a bit wet. Bring a towel!",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[1] if len(users) > 1 else users[0],  # marnie or fallback
            "pokemon": pokemon[3] if len(pokemon) > 3 else pokemon[0],  # Venusaur or fallback
            "rating": 5,
            "title": "Nature at its finest",
            "body": "Venusaur's garden is absolutely beautiful. The aroma from the flower is so calming. Perfect spot for nature lovers!",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[3] if len(users) > 3 else users[0],  # ash or fallback
            "pokemon": pokemon[4] if len(pokemon) > 4 else pokemon[0],  # Gengar or fallback
            "rating": 4,
            "title": "Spooky but fun",
            "body": "Gengar was definitely spooky but in a fun way! The tower has great atmosphere. Just don't go alone at night!",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[2] if len(users) > 2 else users[0],  # bobbie or fallback
            "pokemon": pokemon[5] if len(pokemon) > 5 else pokemon[0],  # Dragonite or fallback
            "rating": 5,
            "title": "Dragon master experience",
            "body": "Dragonite was incredible! So intelligent and graceful. The den location is mystical and the views are spectacular.",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[2] if len(pokemon) > 2 else pokemon[0],  # Blastoise or fallback
            "rating": 3,
            "title": "Good but pricey",
            "body": "Blastoise is great, but the gym charges quite a bit for entry. The experience was good overall, just wish it was more affordable.",
            "created_at": datetime.utcnow()
        }
    ]

    created_reviews = {}
    for data in review_data:
        # Check if review already exists for this user/pokemon combination
        existing_review = Review.query.filter_by(
            user_id=data["user"].id, 
            pokemon_id=data["pokemon"].id
        ).first()
        
        if not existing_review:
            review = Review(
                user_id=data["user"].id,
                pokemon_id=data["pokemon"].id,
                rating=data["rating"],
                title=data["title"],
                body=data["body"],
                created_at=data["created_at"]
            )
            db.session.add(review)
            db.session.flush()
            created_reviews[f"{data['user'].username}_{data['pokemon'].name}"] = review
        else:
            created_reviews[f"{data['user'].username}_{data['pokemon'].name}"] = existing_review

    db.session.commit()
    
    # Return the created reviews for reference
    return created_reviews

def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))
    db.session.commit()
