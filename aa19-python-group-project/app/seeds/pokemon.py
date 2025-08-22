from app.models import db, Pokemon, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_pokemon():
    pokemon_data = [
        {
            "name": "Pikachu",
            "type": "Electric",
            "type_secondary": None,
            "description": "An Electric-type Pokémon that stores energy in its cheeks. It releases this energy when threatened.",
            "region": "Kanto",
            "category": "Mouse Pokémon"
        },
        {
            "name": "Charizard",
            "type": "Fire",
            "type_secondary": "Flying",
            "description": "A powerful Fire/Flying-type Pokémon that can melt boulders with its flames.",
            "region": "Kanto",
            "category": "Flame Pokémon"
        },
        {
            "name": "Blastoise",
            "type": "Water",
            "type_secondary": None,
            "description": "A Water-type Pokémon with powerful water cannons that can blast through steel.",
            "region": "Kanto",
            "category": "Shellfish Pokémon"
        },
        {
            "name": "Venusaur",
            "type": "Grass",
            "type_secondary": "Poison",
            "description": "A Grass/Poison-type Pokémon with a large flower on its back that releases a soothing fragrance.",
            "region": "Kanto",
            "category": "Seed Pokémon"
        },
        {
            "name": "Gengar",
            "type": "Ghost",
            "type_secondary": "Poison",
            "description": "A mischievous Ghost/Poison-type Pokémon that hides in shadows and loves to play pranks.",
            "region": "Kanto",
            "category": "Shadow Pokémon"
        },
        {
            "name": "Dragonite",
            "type": "Dragon",
            "type_secondary": "Flying",
            "description": "A rare Dragon/Flying-type Pokémon known for its intelligence and ability to fly faster than sound.",
            "region": "Johto",
            "category": "Dragon Pokémon"
        }
    ]

    created_pokemon = {}
    for data in pokemon_data:
        # Check if pokemon already exists
        existing_pokemon = Pokemon.query.filter_by(name=data["name"]).first()
        if not existing_pokemon:
            pokemon = Pokemon(**data)
            db.session.add(pokemon)
            db.session.flush()  # Get the ID without committing
            created_pokemon[pokemon.name] = pokemon
        else:
            created_pokemon[existing_pokemon.name] = existing_pokemon
    
    db.session.commit()
    
    # Return the created pokemon for reference in other seeders
    return created_pokemon

def undo_pokemon():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.pokemon RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM pokemon"))
    db.session.commit()
