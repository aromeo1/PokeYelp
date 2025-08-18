from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL


class ImageForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(), Length(max=500)])
    caption = StringField('Caption', validators=[Length(max=255)])
