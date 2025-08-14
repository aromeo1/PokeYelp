from .db import db, environment, SCHEMA, add_prefix_for_prod


class ListPokemon(db.Model):
    __tablename__ = 'list_pokemon'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('lists.id')), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('pokemon.id')), nullable=False)

    # Relationships
    list = db.relationship('List', back_populates='list_pokemon')
    pokemon = db.relationship('Pokemon', back_populates='lists')

    def to_dict(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            'pokemon_id': self.pokemon_id
        }
