from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import TextArea

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    bedrooms = StringField('Number of Bedrooms', validators=[InputRequired(), NumberRange(min=0)])
    bathrooms = StringField('Number of Bathrooms', validators=[InputRequired(), NumberRange(min=0)])
    location = StringField('Location', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired(), NumberRange(min=0)])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()], widget=TextArea())
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'])])
