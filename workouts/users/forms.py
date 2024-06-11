#users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from workouts.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
   
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm',
                                                                             message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
            
            
class UpdateUserForm(FlaskForm):
    email = StringField('Update Email', validators=[Email(), DataRequired()])
    username = StringField('Update Username')
    password = PasswordField('Update Password', validators=[EqualTo('pass_confirm', message='Passwords Must Match!'), DataRequired()])
    pass_confirm = PasswordField('Confirm New Password')
    submit = SubmitField('Update')
    