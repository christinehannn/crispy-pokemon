from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)

from pokemon import db
from pokemon.models import Pokemon
from pokemon.pokemons.forms import PokemonForm
from pokemon.utils import save_picture

pokemons = Blueprint('pokemons', __name__)


@pokemons.route('/pokemon/new', methods=['GET', 'POST'])
@login_required
def new_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon = Pokemon(
            name=form.name.data,
            date_caught=form.date_caught.data,
            type=form.type.data,
            description=form.description.data,
            trainer=current_user,
        )
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)
            pokemon.image_file = image_file
        db.session.add(pokemon)
        db.session.commit()
        flash('Your Pokemon has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template(
        'create_pokemon.html',
        title='New Pokemon',
        form=form,
        legend='New Pokemon'
    )


@pokemons.route('/pokemon/<int:pokemon_id>')
def pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return render_template('pokemon.html', title=pokemon.name, pokemon=pokemon)


@pokemons.route('/pokemon/<int:pokemon_id>/update', methods=['GET', 'POST'])
@login_required
def update_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    if pokemon.trainer != current_user:
        abort(403)
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon.name = form.name.data
        pokemon.date_caught = form.date_caught.data
        pokemon.type = form.type.data
        pokemon.description = form.description.data
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)
            pokemon.image_file = image_file
        db.session.commit()
        flash('Your pokemon has been updated!', 'success')
        return redirect(url_for('pokemons.pokemon', pokemon_id=pokemon.id))
    elif request.method == 'GET':
        form.name.data = pokemon.name
        form.date_caught.data = pokemon.date_caught
        form.type.data = pokemon.type
        form.description.data = pokemon.description
        form.image_file.data = pokemon.image_file
    return render_template(
        'create_pokemon.html',
        title='Update Pokemon',
        form=form,
        legend='Update Pokemon'
    )


@pokemons.route('/pokemon/<int:pokemon_id>/delete', methods=['POST'])
@login_required
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    if pokemon.trainer != current_user:
        abort(403)
    db.session.delete(pokemon)
    db.session.commit()
    flash('Your Pokemon has been deleted!', 'success')
    return redirect(url_for('main.home'))
