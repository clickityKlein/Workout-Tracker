#strength_training/forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField


class StrengthTrainingForm(FlaskForm):
    submit = SubmitField('Log Workout')
            
class UpdateStrengthTrainingForm(FlaskForm):
    workout_name = StringField('Change Workout Name')
    date = DateField('Change Date')
    location = StringField('Change Location')
    submit = SubmitField('Update Workout')
