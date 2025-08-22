from app.models import db, Image, User, Pokemon, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_images():
    # Get actual users and pokemon from the database
    users = User.query.all()
    pokemon = Pokemon.query.all()
    
    if not users or not pokemon:
        print("Warning: No users or pokemon found. Skipping images seeding.")
        return {}
    
    # Create images with actual user and pokemon references
    image_data = [
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[0],  # Pikachu
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[1] if len(users) > 1 else users[0],  # marnie or fallback
            "pokemon": pokemon[1] if len(pokemon) > 1 else pokemon[0],  # Charizard
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[2] if len(users) > 2 else users[0],  # bobbie or fallback
            "pokemon": pokemon[2] if len(pokemon) > 2 else pokemon[0],  # Blastoise
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[3] if len(pokemon) > 3 else pokemon[0],  # Venusaur
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[3] if len(users) > 3 else users[0],  # ash or fallback
            "pokemon": pokemon[4] if len(pokemon) > 4 else pokemon[0],  # Gengar
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[1] if len(users) > 1 else users[0],  # marnie or fallback
            "pokemon": pokemon[5] if len(pokemon) > 5 else pokemon[0],  # Dragonite
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[2] if len(users) > 2 else users[0],  # bobbie or fallback
            "pokemon": pokemon[0],  # Pikachu
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[0],  # Demo user
            "pokemon": pokemon[1] if len(pokemon) > 1 else pokemon[0],  # Charizard
            "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
            "created_at": datetime.utcnow()
        }
    ]

    created_images = []
    for data in image_data:
        if data["user"] and data["pokemon"]:
            # Check if image already exists for this user/pokemon/url combination
            existing_image = Image.query.filter_by(
                user_id=data["user"].id, 
                pokemon_id=data["pokemon"].id,
                url=data["url"]
            ).first()
            
            if not existing_image:
                image = Image(
                    user_id=data["user"].id,
                    pokemon_id=data["pokemon"].id,
                    url=data["url"],
                    created_at=data["created_at"]
                )
                db.session.add(image)
                db.session.flush()
                created_images.append(image)
            else:
                created_images.append(existing_image)

    db.session.commit()
    
    # Return the created images for reference
    return created_images

def undo_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM images"))
    db.session.commit()
