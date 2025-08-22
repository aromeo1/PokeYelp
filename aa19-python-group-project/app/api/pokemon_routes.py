from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Pokemon, Image
from app.forms import PokemonForm

pokemon_routes = Blueprint('pokemon', __name__)

@pokemon_routes.route('/')
def get_all_pokemon():
    pokemon = Pokemon.query.all()
    return jsonify({'pokemon': [p.to_dict() for p in pokemon]})

@pokemon_routes.route('/', methods=['POST'])
@login_required
def create_pokemon():
    form = PokemonForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        pokemon = Pokemon(
            name=form.data['name'],
            type=form.data['type'],
            type_secondary=form.data['type_secondary'],
            region=form.data['region'],
            category=form.data['category'],
            description=form.data['description'],
            user_id=current_user.id
        )
        
        db.session.add(pokemon)
        db.session.commit()
        
        # Create image record if URL is provided
        if form.data['image_url']:
            image = Image(
                url=form.data['image_url'],
                pokemon_id=pokemon.id,
                user_id=current_user.id
            )
            db.session.add(image)
            db.session.commit()
        
        return jsonify(pokemon.to_dict()), 201
    
    return jsonify({'errors': form.errors}), 400

@pokemon_routes.route('/<int:id>')
def get_pokemon_by_id(id):
    pokemon = Pokemon.query.get_or_404(id)
    return jsonify(pokemon.to_dict())

@pokemon_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    
    if pokemon.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = PokemonForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        pokemon.name = form.data['name']
        pokemon.type = form.data['type']
        pokemon.type_secondary = form.data['type_secondary']
        pokemon.region = form.data['region']
        pokemon.category = form.data['category']
        pokemon.description = form.data['description']
        
        db.session.commit()
        return jsonify(pokemon.to_dict())
    
    return jsonify({'errors': form.errors}), 400

@pokemon_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_pokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    
    if pokemon.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Delete associated images (only database records, not files)
    images = Image.query.filter_by(pokemon_id=id).all()
    for image in images:
        db.session.delete(image)
    
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({'message': 'Pokemon deleted successfully'})
