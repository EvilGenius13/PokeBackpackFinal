from sqlalchemy_utils import URLType
from flask_login import UserMixin
from poke_app.extensions import db
from poke_app.utils import FormEnum

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
    FAIRY = 'Fairy'

class Pokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  category = db.Column(db.Enum(PokemonCategory), nullable=False)
  artwork = db.Column(URLType, nullable=False)
  attack = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  hp = db.Column(db.Integer, nullable=False)
  favourited = db.relationship('User', secondary='favourite_pokemon', back_populates='favourite_pokemon')
  
  
class Items(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  artwork = db.Column(URLType, nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.String(500), nullable=False)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(250), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  favourite_pokemon = db.relationship('Pokemon', secondary='favourite_pokemon', back_populates='favourited')

favourite_pokemon_list = db.Table('favourite_pokemon',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)
