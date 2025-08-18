from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Review
from app.forms import ReviewForm

review_routes = Blueprint('reviews', __name__)

@review_routes.route('/pokemon/<int:pokemon_id>/reviews')
def get_pokemon_reviews(pokemon_id):
    reviews = Review.query.filter_by(pokemon_id=pokemon_id).all()
    return jsonify({'reviews': [r.to_dict() for r in reviews]})

@review_routes.route('/pokemon/<int:pokemon_id>/reviews', methods=['POST'])
@login_required
def create_pokemon_review(pokemon_id):
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        review = Review(
            rating=form.data['rating'],
            comment=form.data['comment'],
            pokemon_id=pokemon_id,
            user_id=current_user.id
        )
        
        db.session.add(review)
        db.session.commit()
        return jsonify(review.to_dict()), 201
    
    return jsonify({'errors': form.errors}), 400

@review_routes.route('/<int:id>')
def get_review_by_id(id):
    review = Review.query.get_or_404(id)
    return jsonify(review.to_dict())

@review_routes.route('/<int:id>', methods=['PATCH'])
@login_required
def update_review(id):
    review = Review.query.get_or_404(id)
    
    if review.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        review.rating = form.data['rating']
        review.comment = form.data['comment']
        
        db.session.commit()
        return jsonify(review.to_dict())
    
    return jsonify({'errors': form.errors}), 400

@review_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    
    if review.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})
