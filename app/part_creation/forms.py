from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class NewPartTypeForm(FlaskForm):
    part_name = StringField('Part Name', validators=[DataRequired()])
    submit = SubmitField('Save Name')
