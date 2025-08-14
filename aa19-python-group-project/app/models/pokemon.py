from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(100), nullable=False)
    type_secondary = db.Column(db.String(100))
    region = db.Column(db.String(100))
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='pokemon')
    reviews = db.relationship('Review', back_populates='pokemon', cascade='all, delete-orphan')
    images = db.relationship('Image', back_populates='pokemon', cascade='all, delete-orphan')
    lists = db.relationship('ListPokemon', back_populates='pokemon', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'type_secondary': self.type_secondary,
            'region': self.region,
            'category': self.category,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'reviews': [review.to_dict() for review in self.reviews],
            'images': [image.to_dict() for image in self.images],
            'lists': [list_pokemon.to_dict() for list_pokemon in self.lists]
        }
