import os
import unittest
from poke_app.extensions import app, db
from poke_app import bcrypt
from poke_app.models import Pokemon, PokemonCategory, Items, User
from app import app

"""
Run these tests with the command:
python3 -m unittest poke_app.maintest
"""

#################################################
# Setup
#################################################

def create_user():
    password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
        username = 'Ash',
        password = password,
        email = 'Ash@gmail.com'
    )
    db.session.add(user)
    db.session.commit()

def create_pokemon():
    pokemon = Pokemon(
        id = 1,
        name = 'Bulbasaur',
        category = 'GRASS',
        artwork = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
        attack = 49,
        defense = 49,
        hp = 45
    )
    db.session.add(pokemon)
    db.session.commit()

def create_item():
    item = Items(
        id = 1,
        name = 'Pokeball',
        artwork = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png',
        price = 200,
        description = 'A device for catching wild Pokemon. It is thrown like a ball at a Pokemon, comfortably encapsulating its target.'
    )
    db.session.add(item)
    db.session.commit()

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)
#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
    
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        create_pokemon()
        create_item()
      
    
    def test_homepage_logged_out(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Pokemon of the day:', response_text)
        self.assertIn('Item of the day:', response_text)

    def test_homepage_logged_in(self):
        create_user()
        login(self.app, 'Ash', 'password')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertNotIn('Bulbasaur:', response_text)
        self.assertNotIn('Item of the day:', response_text)

    
    def test_pokemon_detail_logged_in(self):
        create_user()
        login(self.app, 'Ash', 'password')
        response = self.app.get('/pokemon/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Bulbasaur', response_text)
        self.assertIn('PokeDex#: 1', response_text)
        self.assertIn('Type: Grass', response_text)
        self.assertIn('Attack: 49', response_text)
        self.assertIn('Defense: 49', response_text)
        self.assertIn('HP: 45', response_text)

    def test_pokemon_detail_logged_out(self):
        response = self.app.get('/pokemon/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page', response_text)
  
    def test_item_detail_logged_in(self):
        create_user()
        login(self.app, 'Ash', 'password')

        response = self.app.get('/item/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Pokeball', response_text)
        self.assertIn('Price: 200', response_text)
        self.assertIn('Description: A device for catching wild Pokemon. It is thrown like a ball at a Pokemon, comfortably encapsulating its target.', response_text)
    
    def test_item_detail_logged_out(self):
        response = self.app.get('/item/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page', response_text)

    def test_create_pokemon_logged_in(self):
        create_user()
        login(self.app, 'Ash', 'password')

        post_data = {
            'id': 2,
            'name': 'Ivysaur',
            'category': 'GRASS',
            'artwork': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png',
            'attack': 62,
            'defense': 63,
            'hp': 60
        }

        self.app.post('create_pokemon', data=post_data, follow_redirects=True)
        pokemon = Pokemon.query.filter_by(id=2).first()
        self.assertEqual(pokemon.name, 'Ivysaur')
        self.assertEqual(pokemon.attack, 62)
    
    def test_create_pokemon_logged_out(self):
        response = self.app.get('create_pokemon', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page', response_text)

    def test_create_item_logged_in(self):
        create_user()
        login(self.app, 'Ash', 'password')

        post_data = {
            'id': 2,
            'name': 'Greatball',
            'artwork': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/great-ball.png',
            'price': 600,
            'description': 'A good, high-performance Ball that provides a higher Pokemon catch rate than a standard Poke Ball.'
        }

        self.app.post('create_item', data=post_data)
        item = Items.query.filter_by(id=2).first()
        self.assertIsNotNone(item)
        self.assertEqual(item.name, 'Greatball')
        self.assertEqual(item.price, 600)

    def test_create_item_logged_out(self):
        response = self.app.get('create_item', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Please log in to access this page', response_text)


    def test_favourite_pokemon(self):
        create_user()
        login(self.app, 'Ash', 'password')

        response = self.app.get('/pokemon/1', follow_redirects=True)
        self.app.post('/favourite/1', follow_redirects=True)

        new_response = self.app.get('/pokemon/1', follow_redirects=True)
        new_response_text = new_response.get_data(as_text=True)
        self.assertIn('Remove from Favourites', new_response_text)

    def test_unfavourite_pokemon(self):
        create_user()
        login(self.app, 'Ash', 'password')

        response = self.app.get('/pokemon/1', follow_redirects=True)
        self.app.post('/favourite/1', follow_redirects=True)
        self.app.post('/unfavourite/1', follow_redirects=True)

        new_response = self.app.get('/pokemon/1', follow_redirects=True)
        new_response_text = new_response.get_data(as_text=True)
        self.assertIn('Add to Favourites', new_response_text)
