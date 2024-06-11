#cardio_training/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField

class CardioTrainingForm(FlaskForm):
    submit = SubmitField('Log Workout')

class UpdateCardioTrainingForm(FlaskForm):
    workout_name = StringField('Change Workout Name')
    date = DateField('Change Date')
    location = StringField('Change Location')
    submit = SubmitField('Update Workout')
