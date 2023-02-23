from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from poke_app.models import Pokemon, PokemonCategory, User
from poke_app import bcrypt

class PokemonForm(FlaskForm):
    id = FloatField('PokeDex', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    category = SelectField('Type', choices= PokemonCategory.choices(), validators=[DataRequired()])
    artwork = StringField('Artwork', validators=[DataRequired(), URL()])
    attack = FloatField('Attack', validators=[DataRequired()])
    defense = FloatField('Defense', validators=[DataRequired()])
    hp = FloatField('HP', validators=[DataRequired()])
    submit = SubmitField('Add Pokemon')

class ItemsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    artwork = StringField('Artwork', validators=[DataRequired(), URL()])
    price = FloatField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Add Item')

class SignUpForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please try another name.')

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password does not match. Please try again.')

#TODO: Need favourite team table