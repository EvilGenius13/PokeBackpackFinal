import random
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
    potd = random.choice(Pokemon.query.all())
    iotd = random.choice(Items.query.all())
    return render_template('home.html', pokemon=pokemon, items=items, potd=potd, iotd=iotd)

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

@main.route('/pokemon/<int:pokemon_id>/edit', methods=['GET', 'POST'])
def edit_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    form = PokemonForm(obj=pokemon)
    if form.validate_on_submit():
        pokemon.name = form.name.data
        pokemon.category = form.category.data
        pokemon.artwork = form.artwork.data
        pokemon.height = form.height.data
        pokemon.weight = form.weight.data
        db.session.commit()
        flash(f'Pokemon {pokemon.name} has been updated!', 'success')
        return redirect(url_for('main.pokemon', pokemon_id=pokemon.id))
    return render_template('edit_pokemon.html', form=form, pokemon=pokemon)

@main.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
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
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    flash(f'Pokemon {pokemon.name} has been deleted!', 'success')
    return redirect(url_for('main.homepage'))

@main.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
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
            password=hashed_password
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
