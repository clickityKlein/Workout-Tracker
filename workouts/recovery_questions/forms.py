#recovery_questions/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from workouts.models import RecoveryQuestions


class SetRecoveryQuestionsForm(FlaskForm):
    question_choices = ["What’s the name of your parent’s pet?",
                        "What's the name of your first pet?",
                        "What's the name of your favorite book?",
                        "What's the name of your childhood best friend?",
                        "What city were you born in?",
                        "What's your favorite color?",
                        "What's the make and model of your first car?",
                        "What's the name of your high school mascot?",
                        "What's your favorite food?",
                        "What's the name of your favorite teacher?",
                        "What was your nickname?",
                        "What's your favorite hobby?"]
    
    question_1 = SelectField('Question 1', validators=[DataRequired()], choices=question_choices)
    question_2 = SelectField('Question 2', validators=[DataRequired()], choices=question_choices)
    question_3 = SelectField('Question 3', validators=[DataRequired()], choices=question_choices)
    question_4 = SelectField('Question 4', validators=[DataRequired()], choices=question_choices)
    question_5 = SelectField('Question 5', validators=[DataRequired()], choices=question_choices)
    
    answer_1 = PasswordField('Answer 1', validators=[DataRequired(), EqualTo('answer_1_confirm', message='Answers Must Match!')])
    answer_1_confirm = PasswordField('Confirm Answer 1', validators=[DataRequired()])
    answer_2 = PasswordField('Answer 2', validators=[DataRequired(), EqualTo('answer_2_confirm', message='Answers Must Match!')])
    answer_2_confirm = PasswordField('Confirm Answer 2', validators=[DataRequired()])
    answer_3 = PasswordField('Answer 3', validators=[DataRequired(), EqualTo('answer_3_confirm', message='Answers Must Match!')])
    answer_3_confirm = PasswordField('Confirm Answer 3', validators=[DataRequired()])
    answer_4 = PasswordField('Answer 4', validators=[DataRequired(), EqualTo('answer_4_confirm', message='Answers Must Match!')])
    answer_4_confirm = PasswordField('Confirm Answer 4', validators=[DataRequired()])
    answer_5 = PasswordField('Answer 5', validators=[DataRequired(), EqualTo('answer_5_confirm', message='Answers Must Match!')])
    answer_5_confirm = PasswordField('Confirm Answer 5', validators=[DataRequired()])
    
    submit = SubmitField('Set Recovery Questions')
    
class ResetRecoveryQuestionsForm(FlaskForm):
    question_choices = ["What’s the name of your parent’s pet?",
                        "What's the name of your first pet?",
                        "What's the name of your favorite book?",
                        "What's the name of your childhood best friend?",
                        "What city were you born in?",
                        "What's your favorite color?",
                        "What's the make and model of your first car?",
                        "What's the name of your high school mascot?",
                        "What's your favorite food?",
                        "What's the name of your favorite teacher?",
                        "What was your nickname?",
                        "What's your favorite hobby?"]
    
    question_1 = SelectField('Question 1', validators=[DataRequired()], choices=question_choices)
    question_2 = SelectField('Question 2', validators=[DataRequired()], choices=question_choices)
    question_3 = SelectField('Question 3', validators=[DataRequired()], choices=question_choices)
    question_4 = SelectField('Question 4', validators=[DataRequired()], choices=question_choices)
    question_5 = SelectField('Question 5', validators=[DataRequired()], choices=question_choices)
    
    answer_1 = PasswordField('Answer 1', validators=[DataRequired(), EqualTo('answer_1_confirm', message='Answers Must Match!')])
    answer_1_confirm = PasswordField('Confirm Answer 1', validators=[DataRequired()])
    answer_2 = PasswordField('Answer 2', validators=[DataRequired(), EqualTo('answer_2_confirm', message='Answers Must Match!')])
    answer_2_confirm = PasswordField('Confirm Answer 2', validators=[DataRequired()])
    answer_3 = PasswordField('Answer 3', validators=[DataRequired(), EqualTo('answer_3_confirm', message='Answers Must Match!')])
    answer_3_confirm = PasswordField('Confirm Answer 3', validators=[DataRequired()])
    answer_4 = PasswordField('Answer 4', validators=[DataRequired(), EqualTo('answer_4_confirm', message='Answers Must Match!')])
    answer_4_confirm = PasswordField('Confirm Answer 4', validators=[DataRequired()])
    answer_5 = PasswordField('Answer 5', validators=[DataRequired(), EqualTo('answer_5_confirm', message='Answers Must Match!')])
    answer_5_confirm = PasswordField('Confirm Answer 5', validators=[DataRequired()])
    
    submit = SubmitField('Reset Recovery Questions')

class AnswerRecoveryQuestionsForm(FlaskForm):
    answer_1 = StringField('Answer 1', validators=[DataRequired()])
    answer_2 = StringField('Answer 2', validators=[DataRequired()])
    answer_3 = StringField('Answer 3', validators=[DataRequired()])
    answer_4 = StringField('Answer 4', validators=[DataRequired()])
    answer_5 = StringField('Answer 5', validators=[DataRequired()])
    submit = SubmitField('Recover Account')
    
class StartRecoveryQuestionsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('To Questions')
