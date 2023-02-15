from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from poke_app.models import Pokemon, Items, Users, PokemonCategory
from poke_app import bcrypt

class PokemonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    category = SelectField('Category', choices=[(tag, tag.value) for tag in PokemonCategory], validators=[DataRequired()])
    artwork = StringField('Artwork', validators=[DataRequired(), URL()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    submit = SubmitField('Add Pokemon')

class ItemsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    artwork = StringField('Artwork', validators=[DataRequired(), URL()])
    price = FloatField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Add Item')

class UsersForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Add User')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Username does not exist')

    def validate_password(self, password):
        user = Users.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Incorrect password')

class FavouritePokemonForm(FlaskForm):
    pokemon = QuerySelectField(query_factory=lambda: Pokemon.query.all(), get_label='name')
    submit = SubmitField('Add to Favourites')




