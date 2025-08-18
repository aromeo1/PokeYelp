from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, List, ListPokemon, Pokemon
from app.forms import ListForm

list_routes = Blueprint('lists', __name__)

# GET /lists - Get all lists
@list_routes.route('/')
def get_all_lists():
    """Get all lists"""
    lists = List.query.all()
    return jsonify({'lists': [l.to_dict() for l in lists]})

# POST /lists - Create a list
@list_routes.route('/', methods=['POST'])
@login_required
def create_list():
    """Create a new list"""
    form = ListForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        list_item = List(
            name=form.data['name'],
            description=form.data['description'],
            user_id=current_user.id
        )
        
        db.session.add(list_item)
        db.session.commit()
        return jsonify(list_item.to_dict()), 201
    
    return jsonify({'errors': form.errors}), 400

# GET /lists/:id - Get a specific list
@list_routes.route('/<int:id>')
def get_list_by_id(id):
    """Get a specific list"""
    list_item = List.query.get_or_404(id)
    return jsonify(list_item.to_dict())

# PATCH /lists/:id - Update a list
@list_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_list(id):
    """Update a list"""
    list_item = List.query.get_or_404(id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = ListForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        list_item.name = form.data['name']
        list_item.description = form.data['description']
        
        db.session.commit()
        return jsonify(list_item.to_dict())
    
    return jsonify({'errors': form.errors}), 400

# DELETE /lists/:id - Delete a list
@list_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_list(id):
    """Delete a list"""
    list_item = List.query.get_or_404(id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(list_item)
    db.session.commit()
    return jsonify({'message': 'List deleted successfully'})

# POST /lists/:id/pokemon/:pokemon_id - Add Pokémon to list
@list_routes.route('/<int:list_id>/pokemon/<int:pokemon_id>', methods=['POST'])
@login_required
def add_pokemon_to_list(list_id, pokemon_id):
    """Add a Pokémon to a list"""
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    
    # Check if already in list
    existing = ListPokemon.query.filter_by(
        list_id=list_id, pokemon_id=pokemon_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Pokemon already in list'}), 400
    
    list_pokemon = ListPokemon(
        list_id=list_id,
        pokemon_id=pokemon_id
    )
    
    db.session.add(list_pokemon)
    db.session.commit()
    
    return jsonify({'message': 'Pokemon added to list'}), 201

# DELETE /lists/:id/pokemon/:pokemon_id - Remove Pokémon from list
@list_routes.route('/<int:list_id>/pokemon/<int:pokemon_id>', methods=['DELETE'])
@login_required
def remove_pokemon_from_list(list_id, pokemon_id):
    """Remove a Pokémon from a list"""
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    list_pokemon = ListPokemon.query.filter_by(
        list_id=list_id, pokemon_id=pokemon_id
    ).first_or_404()
    
    db.session.delete(list_pokemon)
    db.session.commit()
    
    return jsonify({'message': 'Pokemon removed from list'})
