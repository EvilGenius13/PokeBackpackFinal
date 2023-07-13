import os
from unittest import TestCase
from datetime import datetime
from poke_app.extensions import app, db
from poke_app import bcrypt
from poke_app.models import Pokemon, PokemonCategory, Items, User
from app import app

"""
Run these tests with the command:
python3 -m unittest poke_app.authtest
"""

#################################################
# Setup
#################################################

def create_user():
    password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
        username = 'testuser',
        password = password,
        email = 'test@gmail.com',
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

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

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

    def test_login(self):
        """Test login page."""
        result = self.app.get('/login', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Login', result.data)

    def test_signup(self):
        password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        post_data = {
            "username": "me1",
            "password": password_hash,
            "email": "me1@test.com",
        }
        self.app.post('/signup', data=post_data)
        new_user = User.query.filter_by(username="me1").one()
        self.assertEqual(new_user.username, "me1")

    def test_login_success(self):
        create_user()
        post_data = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(post_data.status_code, 200)
        self.assertIn(b'Logout', post_data.data)

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = (self.app.post('/login', data=post_data, follow_redirects=True))
        response_text = response.get_data(as_text=True)
        self.assertIn("Password does not match. Please try again.", response_text)

    def test_logout(self):
        create_user()
        login = self.app.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(login.status_code, 200)
        self.assertIn(b'Logout', login.data)
        logout = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(logout.status_code, 200)
        self.assertIn(b'Login', logout.data)

    def test_signup_duplicate_username(self):
        create_user()
        password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        post_data = {
            "username": "testuser",
            "password": password_hash,
            "email": "test@gmail.com'",
        }
        result = self.app.post('/signup', data=post_data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Username already exists. Please try another name.', result.data)

    def test_login_nonexistent_user(self):
        post_data = {
            "username": "idontexist",
            "password": "password"
        }
        response = (self.app.post('/login', data=post_data, follow_redirects=True))
        response_text = response.get_data(as_text=True)
        self.assertIn("No user with that username. Please try again.", response_text)

    