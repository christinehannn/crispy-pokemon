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

pokemons = Blueprint('pokemons', __name__)


@pokemons.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PokemonForm()
    if form.validate_on_submit():
        pokemon = Pokemon(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template(
        'create_post.html',
        title='New Post',
        form=form,
        legend='New Post'
    )


@pokemons.route('/post/<int:post_id>')
def post(post_id):
    post = Pokemon.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@pokemons.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Pokemon.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PokemonForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        'create_post.html',
        title='Update Post',
        form=form,
        legend='Update Post'
    )


@pokemons.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Pokemon.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
