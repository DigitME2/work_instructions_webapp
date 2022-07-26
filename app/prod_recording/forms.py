from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class NewBatchForm(FlaskForm):
    part_type = SelectField('Part Type')
    amount = IntegerField('Number of parts', validators=[DataRequired()])
    batch_number = StringField('Batch Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
