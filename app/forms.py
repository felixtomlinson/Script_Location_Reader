from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms.validators import Email, DataRequired
from wtforms import StringField, SubmitField, FileField


class ScriptForm(FlaskForm):
    # email_address = StringField(validators=[Email(), DataRequired()])
    script = FileField(validators=[FileRequired()])
    submit = SubmitField()
