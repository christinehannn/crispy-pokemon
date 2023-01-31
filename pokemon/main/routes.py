from flask import (
    Blueprint,
    render_template,
    request,
)

from pokemon.models import Pokemon

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    pokemons = Pokemon.query.order_by(
        Pokemon.date_created.desc()
    ).paginate(
        page=page,
        per_page=5
    )
    return render_template('home.html', pokemons=pokemons)
