from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, URL


class PokemonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=255)])
    type = StringField('Type', validators=[DataRequired(), Length(min=1, max=100)])
    type_secondary = StringField('Secondary Type', validators=[Optional(), Length(max=100)])
    region = StringField('Region', validators=[Optional(), Length(max=100)])
    category = StringField('Category', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    image_url = StringField('Image URL', validators=[Optional(), URL(), Length(max=500)])
