from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class PokemonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    type = StringField('Type', validators=[DataRequired(), Length(min=1, max=50)])
    abilities = StringField('Abilities', validators=[DataRequired(), Length(min=1, max=200)])
    height = IntegerField('Height', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
