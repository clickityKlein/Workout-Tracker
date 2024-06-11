#strength_training_sub/forms.py
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import IntegerField, SubmitField, StringField, DateField
from datetime import datetime

# workout_name - String
# date - Date
# location - String
# exercise_count - Integer
# set_count - Integer


class StrengthTrainingSubForm(FlaskForm):
    workout_name = StringField('Workout Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location')
    exercise_count = IntegerField('Number of Exercises', validators=[DataRequired()])
    set_count = IntegerField('Number of Sets', validators=[DataRequired()])
    submit = SubmitField('Create Workout')