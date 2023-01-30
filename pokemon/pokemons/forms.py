from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileAllowed,
    FileField,
)
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    DateTimeField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
)


class PokemonForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type')
    description = TextAreaField('Description', validators=[DataRequired()])
    image_file = FileField(
        'Upload Pokemon picture',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    date_caught = DateTimeField(
        'Date Caught',
        format='%m/%d/%Y',
        validators=[Optional()]
    )
    submit = SubmitField('Save')
