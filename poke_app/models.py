from poke_app.extensions import db
from poke_app.utils import FormEnum
from sqlalchemy_utils import URLType
from flask_login import UserMixin


class PokemonCategory(FormEnum):
    NORMAL = 'Normal'
    FIRE = 'Fire'
    WATER = 'Water'
    ELECTRIC = 'Electric'
    GRASS = 'Grass'
    ICE = 'Ice'
    FIGHTING = 'Fighting'
    POISON = 'Poison'
    GROUND = 'Ground'
    FLYING = 'Flying'
    PSYCHIC = 'Psychic'
    BUG = 'Bug'
    ROCK = 'Rock'
    GHOST = 'Ghost'
    DRAGON = 'Dragon'

class Pokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  category = db.Column(db.Enum(PokemonCategory), nullable=False)
  artwork = db.Column(URLType, nullable=False)
  height = db.Column(db.Float, nullable=False)
  weight = db.Column(db.Float, nullable=False)
  favourite_pokemon_pokemon = db.relationship('Users', secondary='favourite_pokemon', backref='favourite_pokemon_pokemon')
  
class Items(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  artwork = db.Column(URLType, nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.Text, nullable=False)

class Users(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(50), nullable=False)
  favourite_pokemon_users = db.relationship('Pokemon', secondary='favourite_pokemon', backref='favourite_pokemon_users')


favourite_pokemon = db.Table('favourite_pokemon',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
  db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
)

