from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Pokemon
from app.forms import PokemonForm

pokemon_routes = Blueprint('pokemon', __name__)

# GET /pokemon - List all Pokémon
@pokemon_routes.route('/')
def get_all_pokemon():
    """List all Pokémon"""
    pokemon = Pokemon.query.all()
    return jsonify({'pokemon': [p.to_dict() for p in pokemon]})

# POST /pokemon - Add a Pokémon
@pokemon_routes.route('/', methods=['POST'])
@login_required
def create_pokemon():
    """Add a new Pokémon"""
    form = PokemonForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        pokemon = Pokemon(
            name=form.data['name'],
            type=form.data['type'],
            abilities=form.data['abilities'],
            height=form.data['height'],
            weight=form.data['weight'],
            description=form.data['description'],
            user_id=current_user.id
        )
        
        db.session.add(pokemon)
        db.session.commit()
        return jsonify(pokemon.to_dict()), 201
    
    return jsonify({'errors': form.errors}), 400

# GET /pokemon/:id - View one Pokémon
@pokemon_routes.route('/<int:id>')
def get_pokemon_by_id(id):
    """View one Pokémon"""
    pokemon = Pokemon.query.get_or_404(id)
    return jsonify(pokemon.to_dict())

# PATCH /pokemon/:id - Update Pokémon
@pokemon_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_pokemon(id):
    """Update a Pokémon"""
    pokemon = Pokemon.query.get_or_404(id)
    
    if pokemon.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = PokemonForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        pokemon.name = form.data['name']
        pokemon.type = form.data['type']
        pokemon.abilities = form.data['abilities']
        pokemon.height = form.data['height']
        pokemon.weight = form.data['weight']
        pokemon.description = form.data['description']
        
        db.session.commit()
        return jsonify(pokemon.to_dict())
    
    return jsonify({'errors': form.errors}), 400

# DELETE /pokemon/:id - Delete Pokémon
@pokemon_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_pokemon(id):
    """Delete a Pokémon"""
    pokemon = Pokemon.query.get_or_404(id)
    
    if pokemon.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({'message': 'Pokemon deleted successfully'})
