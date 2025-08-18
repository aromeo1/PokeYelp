from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Image, Pokemon
from app.forms import ImageForm

image_routes = Blueprint('images', __name__)

# GET /images - Get all images
@image_routes.route('/')
def get_all_images():
    """Get all images"""
    images = Image.query.all()
    return jsonify({'images': [i.to_dict() for i in images]})

# GET /images/:id - Get a specific image
@image_routes.route('/<int:id>')
def get_image_by_id(id):
    """Get a specific image"""
    image = Image.query.get_or_404(id)
    return jsonify(image.to_dict())

# GET /pokemon/:id/images - Get all images for a Pokémon
@image_routes.route('/pokemon/<int:pokemon_id>')
def get_pokemon_images(pokemon_id):
    """Get all images for a specific Pokémon"""
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    images = Image.query.filter_by(pokemon_id=pokemon_id).all()
    return jsonify({'images': [i.to_dict() for i in images]})

# POST /pokemon/:id/images - Upload an image for a Pokémon
@image_routes.route('/pokemon/<int:pokemon_id>', methods=['POST'])
@login_required
def upload_pokemon_image(pokemon_id):
    """Upload an image for a Pokémon"""
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    
    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        image = Image(
            url=form.data['url'],
            caption=form.data['caption'],
            pokemon_id=pokemon_id,
            user_id=current_user.id
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify(image.to_dict()), 201
    
    return jsonify({'errors': form.errors}), 400

# PATCH /images/:id - Update an image
@image_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_image(id):
    """Update an image"""
    image = Image.query.get_or_404(id)
    
    if image.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        image.url = form.data['url']
        image.caption = form.data['caption']
        
        db.session.commit()
        return jsonify(image.to_dict())
    
    return jsonify({'errors': form.errors}), 400

# DELETE /images/:id - Delete an image
@image_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_image(id):
    """Delete an image"""
    image = Image.query.get_or_404(id)
    
    if image.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': 'Image deleted successfully'})
