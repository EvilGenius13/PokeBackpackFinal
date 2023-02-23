import random
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from poke_app.models import Pokemon, Items, User
from poke_app.forms import PokemonForm, ItemsForm, SignUpForm, LoginForm
from poke_app import bcrypt
from poke_app.extensions import app, db
import requests

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

colours = {
    'Normal': '#A8A77A',
    'Fire': '#EE8130',
    'Water': '#6390F0',
    'Electric': '#F7D02C',
    'Grass': '#7AC74C',
    'Ice': '#96D9D6',
    'Fighting': '#c03028',
    'Poison': '#A33EA1',
    'Ground': '#E2BF65',
    'Flying': '#A98FF3',
    'Psychic': '#F95587',
    'Bug': '#A6B91A',
    'Rock': '#B6A136',
    'Ghost': '#705898',
    'Dragon': '#6F35FC',
    'Fairy': '#D685AD'
}

#! Routes Below this line
#------------------------------------------------------------#

@main.route('/')
def homepage():
    pokemon = Pokemon.query.all()
    items = Items.query.all()
    potd = random.choice(Pokemon.query.all())
    iotd = random.choice(Items.query.all())
    return render_template('home.html', pokemon=pokemon, items=items, potd=potd, iotd=iotd)

@main.route('/create_pokemon', methods=['GET', 'POST'])
@login_required
def create_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        new_pokemon= Pokemon(
            id = form.id.data,
            name = form.name.data,
            category = form.category.data,
            artwork = form.artwork.data,
            attack = form.attack.data,
            defense = form.defense.data,
            hp = form.hp.data
        )
        db.session.add(new_pokemon)
        db.session.commit()
        flash(f'Pokemon {new_pokemon.name} has been created!', 'success')
        return redirect(url_for('main.pokemon', pokemon_id=new_pokemon.id))
    return render_template('create_pokemon.html', form=form)

@main.route('/create_item', methods=['GET', 'POST'])
@login_required
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
@login_required
def pokemon(pokemon_id):
    colour = ''
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    for key, value in colours.items():
        if str(pokemon.category) == str(key):
            colour = value
    return render_template('pokemon_details.html', pokemon=pokemon, colour=colour)

@main.route('/item/<int:item_id>')
@login_required
def item(item_id):
    item = Items.query.get_or_404(item_id)
    return render_template('item_details.html', item=item)

@main.route('/pokemon/<int:pokemon_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    form = PokemonForm(obj=pokemon)
    if form.validate_on_submit():
        pokemon.name = form.name.data
        pokemon.category = form.category.data
        pokemon.artwork = form.artwork.data
        pokemon.attack = form.attack.data
        pokemon.defense = form.defense.data
        pokemon.hp = form.hp.data
        db.session.commit()
        flash(f'Pokemon {pokemon.name} has been updated!', 'success')
        return redirect(url_for('main.pokemon', pokemon_id=pokemon.id))
    return render_template('edit_pokemon.html', form=form, pokemon=pokemon)

@main.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Items.query.get_or_404(item_id)
    form = ItemsForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.artwork = form.artwork.data
        item.price = form.price.data
        item.description = form.description.data
        db.session.commit()
        flash(f'Item {item.name} has been updated!', 'success')
        return redirect(url_for('main.item', item_id=item.id))
    return render_template('edit_item.html', form=form, item=item)

@main.route('/pokemon/<int:pokemon_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    flash(f'Pokemon {pokemon.name} has been deleted!', 'success')
    return redirect(url_for('main.homepage'))

@main.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = Items.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'Item {item.name} has been deleted!', 'success')
    return redirect(url_for('main.homepage'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            password=hashed_password,
            email=form.email.data 
            )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        flash('You have been logged in!', 'success')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.homepage'))

@main.route('/filldata', methods=['GET', 'POST'])
def filldata():
    POKE_API = 'https://pokeapi.co/api/v2/pokemon/'
    ITEM_API = 'https://pokeapi.co/api/v2/item/'
    for i in range(1, 152):
        response = requests.get(POKE_API + str(i))
        data = response.json()
        pokemon = Pokemon(
            id = i,
            name = data['name'],
            category = data['types'][0]['type']['name'].upper(),
            artwork = data['sprites']['front_default'],
            attack = data['stats'][4]['base_stat'],
            defense = data['stats'][3]['base_stat'],
            hp = data['stats'][5]['base_stat']
        )
        db.session.add(pokemon)
        db.session.commit()
        flash('Data has been filled!', 'success')
    for i in range(1, 51):
        response = requests.get(ITEM_API + str(i))
        data = response.json()
        item = Items(
            id = i,
            name = data['name'],
            artwork = data['sprites']['default'],
            price = random.randint(100, 1000),
            description = data['effect_entries'][0]['effect']
        )
        db.session.add(item)
        db.session.commit()
        flash('Data has been filled!', 'success')
    return redirect(url_for('main.homepage'))

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@main.route('/favourite/<int:pokemon_id>', methods=['POST'])
@login_required
def favourite(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    team_length = len(current_user.favourite_pokemon)
    if team_length >= 6:
        flash(f'You can only have 6 favourite pokemon!', 'danger')
        return redirect(url_for('main.pokemon', pokemon_id=pokemon.id))
    else:
        current_user.favourite_pokemon.append(pokemon)
    db.session.commit()
    flash(f'Pokemon {pokemon.name} has been added to your favourites!', 'success')
    return redirect(url_for('main.pokemon', pokemon_id=pokemon.id))

@main.route('/unfavourite/<int:pokemon_id>', methods=['POST'])
@login_required
def unfavourite(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    current_user.favourite_pokemon.remove(pokemon)
    db.session.commit()
    flash(f'Pokemon {pokemon.name} has been removed from your favourites!', 'success')
    return redirect(url_for('main.pokemon', pokemon_id=pokemon.id))