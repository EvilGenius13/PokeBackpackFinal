from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from poke_app.models import Pokemon, Items, User
from poke_app.forms import PokemonForm, ItemsForm, SignUpForm, LoginForm
from poke_app import bcrypt
from poke_app.extensions import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

#! Routes Below this line
#------------------------------------------------------------#

@main.route('/')
def homepage():
    pokemon = Pokemon.query.all()
    items = Items.query.all()
    return render_template('home.html', pokemon=pokemon, items=items)

@main.route('/create_pokemon', methods=['GET', 'POST'])
def create_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        new_pokemon= Pokemon(
            id = form.id.data,
            name = form.name.data,
            category = form.category.data,
            artwork = form.artwork.data,
            height = form.height.data,
            weight = form.weight.data
        )
        db.session.add(new_pokemon)
        db.session.commit()
        flash(f'Pokemon {new_pokemon.name} has been created!', 'success')
        return redirect(url_for('main.pokemon', pokemon_id=new_pokemon.id))
    return render_template('create_pokemon.html', form=form)

@main.route('/create_item', methods=['GET', 'POST'])
def create_item():
    form = ItemsForm()
    if form.validate_on_submit():
        new_item= Items(
            name = form.name.data,
            artwork = form.artwork.data,
            price = form.price.data,
            description = form.description.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash(f'Item {new_item.name} has been created!', 'success')
        return redirect(url_for('main.item', item_id=new_item.id))
    return render_template('create_item.html', form=form)

@main.route('/pokemon/<int:pokemon_id>')
def pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return render_template('pokemon_details.html', pokemon=pokemon)

@main.route('/item/<int:item_id>')
def item(item_id):
    item = Items.query.get_or_404(item_id)
    return render_template('item_details.html', item=item)

