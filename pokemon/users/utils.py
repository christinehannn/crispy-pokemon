from flask import (
    url_for,
)

from pokemon.utils import send_mailgun_email


def send_reset_email(user):
    token = user.get_reset_token()
    body = (
        f'To reset your password, visit the following link: '
        f'{url_for("users.reset_token", token=token, _external=True)}\n'
        'If you did not make this request then simply ignore this email and '
        'no changes will be made.'
    )
    send_mailgun_email(
        user.email,
        'Password Reset Request',
        body
    )
