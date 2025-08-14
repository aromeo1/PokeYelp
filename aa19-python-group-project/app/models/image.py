from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Image(db.Model):
    __tablename__ = 'images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('pokemon.id')), nullable=False)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='images')
    pokemon = db.relationship('Pokemon', back_populates='images')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pokemon_id': self.pokemon_id,
            'url': self.url,
            'created_at': self.created_at.isoformat()
        }
