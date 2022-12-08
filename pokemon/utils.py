import os
import requests


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
