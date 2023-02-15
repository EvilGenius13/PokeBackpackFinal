from flask import Flask, render_template, url_for, redirect, flash, request, Blueprint
#from poke_app.forms import PokemonForm, ItemsForm, UsersForm, SignUpForm, LoginForm, FavouritePokemonForm
from poke_app.models import Pokemon, Items, Users
from flask_login import login_user, logout_user, login_required, current_user

from poke_app.extensions import app, db
from poke_app import bcrypt


main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pokemon')
def pokemon():
    #pokemon = Pokemon.query.all()
    #return render_template('pokemon.html', pokemon=pokemon)
    return render_template('pokemon.html')
