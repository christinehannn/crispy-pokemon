import os
import secrets

import requests
from PIL import Image
from flask import current_app


def send_mailgun_email(
    to,
    subject,
    body,
    sender='No Reply <noreply@email.com>'
):
    requests.post(
        f'{os.getenv("MAILGUN_API_BASE_URL")}/messages',
        auth=('api', os.getenv('MAILGUN_API_KEY')),
        data={
            'from': sender,
            'to': to,
            'subject': subject,
            'text': body,
        }
    )


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path,
        'static/profile_pics',
        picture_fn
    )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
