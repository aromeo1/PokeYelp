from app.models import db, List, ListPokemon, User, Pokemon, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_lists():
    # Get actual users and pokemon from the database
    users = User.query.all()
    pokemon = Pokemon.query.all()
    
    if not users or not pokemon:
        print("Warning: No users or pokemon found. Skipping lists seeding.")
        return {}
    
    # Create lists with actual user references
    list_data = [
        {
            "user": users[0],  # Demo user
            "name": "My Favorite Electric Types",
            "description": "A collection of the best electric Pokemon I've encountered",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[0],  # Demo user
            "name": "Starter Pokemon Collection",
            "description": "All the starter Pokemon from different regions",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[1] if len(users) > 1 else users[0],  # marnie or fallback
            "name": "Fire Type Masters",
            "description": "The hottest fire type Pokemon around",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[2] if len(users) > 2 else users[0],  # bobbie or fallback
            "name": "Water Adventures",
            "description": "Best water Pokemon for aquatic adventures",
            "created_at": datetime.utcnow()
        },
        {
            "user": users[3] if len(users) > 3 else users[0],  # ash or fallback
            "name": "Ghostly Encounters",
            "description": "Spooky ghost type Pokemon I've met",
            "created_at": datetime.utcnow()
        }
    ]

    created_lists = {}
    for data in list_data:
        # Check if list already exists
        existing_list = List.query.filter_by(name=data["name"], user_id=data["user"].id).first()
        if not existing_list:
            list_obj = List(
                user_id=data["user"].id,
                name=data["name"],
                description=data["description"],
                created_at=data["created_at"]
            )
            db.session.add(list_obj)
            db.session.flush()
            created_lists[data["name"]] = list_obj
        else:
            created_lists[data["name"]] = existing_list

    db.session.commit()

    # Create list-pokemon relationships with actual pokemon references
    list_pokemon_data = [
        {"list": created_lists["My Favorite Electric Types"], "pokemon": pokemon[0]},  # Pikachu
        {"list": created_lists["Starter Pokemon Collection"], "pokemon": pokemon[1] if len(pokemon) > 1 else pokemon[0]},  # Charizard
        {"list": created_lists["Starter Pokemon Collection"], "pokemon": pokemon[2] if len(pokemon) > 2 else pokemon[0]},  # Blastoise
        {"list": created_lists["Starter Pokemon Collection"], "pokemon": pokemon[3] if len(pokemon) > 3 else pokemon[0]},  # Venusaur
        {"list": created_lists["Fire Type Masters"], "pokemon": pokemon[1] if len(pokemon) > 1 else pokemon[0]},  # Charizard
        {"list": created_lists["Water Adventures"], "pokemon": pokemon[2] if len(pokemon) > 2 else pokemon[0]},  # Blastoise
        {"list": created_lists["Water Adventures"], "pokemon": pokemon[5] if len(pokemon) > 5 else pokemon[0]},  # Dragonite
        {"list": created_lists["Ghostly Encounters"], "pokemon": pokemon[4] if len(pokemon) > 4 else pokemon[0]},  # Gengar
    ]

    created_relationships = []
    for data in list_pokemon_data:
        if data["list"] and data["pokemon"]:
            # Check if relationship already exists
            existing_rel = ListPokemon.query.filter_by(
                list_id=data["list"].id, 
                pokemon_id=data["pokemon"].id
            ).first()
            
            if not existing_rel:
                list_pokemon = ListPokemon(
                    list_id=data["list"].id,
                    pokemon_id=data["pokemon"].id
                )
                db.session.add(list_pokemon)
                created_relationships.append(list_pokemon)

    db.session.commit()
    
    # Return the created lists for reference
    return created_lists

def undo_lists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.list_pokemon RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.lists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM list_pokemon"))
        db.session.execute(text("DELETE FROM lists"))
    db.session.commit()
