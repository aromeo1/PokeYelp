from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, List, ListPokemon, Pokemon
from app.forms import ListForm

list_routes = Blueprint('lists', __name__)

@list_routes.route('/')
def get_all_lists():
    lists = List.query.all()
    return jsonify({'lists': [l.to_dict() for l in lists]})

@list_routes.route('/', methods=['POST'])
@login_required
def create_list():
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

@list_routes.route('/<int:id>')
def get_list_by_id(id):
    list_item = List.query.get_or_404(id)
    return jsonify(list_item.to_dict())

@list_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_list(id):
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

@list_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_list(id):
    list_item = List.query.get_or_404(id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(list_item)
    db.session.commit()
    return jsonify({'message': 'List deleted successfully'})

@list_routes.route('/<int:list_id>/pokemon/<int:pokemon_id>', methods=['POST'])
@login_required
def add_pokemon_to_list(list_id, pokemon_id):
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    
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

@list_routes.route('/<int:list_id>/pokemon/<int:pokemon_id>', methods=['DELETE'])
@login_required
def remove_pokemon_from_list(list_id, pokemon_id):
    list_item = List.query.get_or_404(list_id)
    
    if list_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    list_pokemon = ListPokemon.query.filter_by(
        list_id=list_id, pokemon_id=pokemon_id
    ).first_or_404()
    
    db.session.delete(list_pokemon)
    db.session.commit()
    
    return jsonify({'message': 'Pokemon removed from list'})
