#models.py
from workouts import db, login_manager
from workouts import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer
from workouts import app
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # table name
    __tablename__ = 'users'

    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # relationships
    strength_workouts_sub = db.relationship('StrengthTrainingSub', backref='athlete', lazy=True)
    strength_workouts = db.relationship('StrengthTraining', backref='athlete', lazy=True)
    cardio_workouts_sub = db.relationship('CardioTrainingSub', backref='athlete', lazy=True)
    cardio_workouts = db.relationship('CardioTraining', backref='athlete', lazy=True)
    recovery_questions = db.relationship('RecoveryQuestions', backref='athlete', lazy=True)

    # instance
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    # functions
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class RecoveryQuestions(db.Model):
    # table name
    __tablename__ = 'recovery_questions'

    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_1 = db.Column(db.String)
    question_2 = db.Column(db.String)
    question_3 = db.Column(db.String)
    question_4 = db.Column(db.String)
    question_5 = db.Column(db.String)
    answer_1_hash = db.Column(db.String)
    answer_2_hash = db.Column(db.String)
    answer_3_hash = db.Column(db.String)
    answer_4_hash = db.Column(db.String)
    answer_5_hash = db.Column(db.String)

    # relationships
    users = db.relationship(User)

    # instance
    def __init__(self, user_id,
                 question_1, question_2, question_3, question_4, question_5,
                 answer_1, answer_2, answer_3, answer_4, answer_5):
        self.user_id = user_id
        self.question_1 = question_1
        self.question_2 = question_2
        self.question_3 = question_3
        self.question_4 = question_4
        self.question_5 = question_5
        self.answer_1_hash = generate_password_hash(answer_1)
        self.answer_2_hash = generate_password_hash(answer_2)
        self.answer_3_hash = generate_password_hash(answer_3)
        self.answer_4_hash = generate_password_hash(answer_4)
        self.answer_5_hash = generate_password_hash(answer_5)
        

    # functions
    def check_answer_1(self, answer_1):
        return check_password_hash(self.answer_1_hash, answer_1)
    
    def check_answer_2(self, answer_2):
        return check_password_hash(self.answer_2_hash, answer_2)
    
    def check_answer_3(self, answer_3):
        return check_password_hash(self.answer_3_hash, answer_3)
    
    def check_answer_4(self, answer_4):
        return check_password_hash(self.answer_4_hash, answer_4)
    
    def check_answer_5(self, answer_5):
        return check_password_hash(self.answer_5_hash, answer_5)


class StrengthTrainingSub(db.Model):
    # table name
    __tablename__ = 'strength_training_sub'
    
    # relationships
    users = db.relationship(User)
    
    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String, nullable=False)
    exercise_count = db.Column(db.Integer, nullable=False)
    set_count = db.Column(db.Integer, nullable=False)
    
    # instance
    def __init__(self, workout_name, date, location, exercise_count, set_count, user_id):
        self.workout_name = workout_name
        self.date = date
        self.location = location
        self.exercise_count = exercise_count
        self.set_count = set_count
        self.user_id = user_id
        
    # functions


class StrengthTraining(db.Model):
    # table name
    __tablename__ = 'strength_training'
    
    # relationships
    users = db.relationship(User)
    

    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String, nullable=False)
    exercise = db.Column(db.String(140), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    order_in_set = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    exercise_count = db.Column(db.Integer, nullable=False)
    set_count = db.Column(db.Integer, nullable=False)
    sub_id = db.Column(db.Integer, nullable=False)
    
    # instance
    def __init__(self, workout_name, date, location, exercise, weight,
                 metric, repetitions, set_number, order_in_set, notes,
                 exercise_count, set_count, user_id, sub_id):
        self.workout_name = workout_name
        self.date = date
        self.location = location
        self.exercise = exercise
        self.weight = weight
        self.metric = metric
        self.repetitions = repetitions
        self.set_number = set_number
        self.order_in_set = order_in_set
        self.notes = notes
        self.exercise_count = exercise_count
        self.set_count = set_count
        self.user_id = user_id
        self.sub_id = sub_id
        
    # functions


class CardioTrainingSub(db.Model):
    # table name
    __tablename__ = 'cardio_training_sub'
    
    # relationships
    users = db.relationship(User)
    
    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String, nullable=False)
    exercise_count = db.Column(db.Integer, nullable=False)
    circuit_count = db.Column(db.Integer, nullable=False)
    
    # instance
    def __init__(self, workout_name, date, location, exercise_count, circuit_count, user_id):
        self.workout_name = workout_name
        self.date = date
        self.location = location
        self.exercise_count = exercise_count
        self.circuit_count = circuit_count
        self.user_id = user_id
        
    # functions
    

class CardioTraining(db.Model):
    # table name
    __tablename__ = 'cardio_training'

    # relationships
    users = db.relationship(User)
    
    # specific columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String, nullable=False)
    exercise = db.Column(db.String(140), nullable=False)
    split = db.Column(db.String, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    metric = db.Column(db.String, nullable=False)
    circuit = db.Column(db.Integer, nullable=False)
    order_in_circuit = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    circuit_count = db.Column(db.Integer, nullable=False)
    exercise_count = db.Column(db.Integer, nullable=False)
    sub_id = db.Column(db.Integer, nullable=False)
    
    # instance
    def __init__(self, workout_name, date, location, exercise, split, distance,
                 metric, circuit, order_in_circuit, notes, circuit_count,
                 exercise_count, sub_id, user_id):
        self.workout_name = workout_name
        self.date = date
        self.location = location
        self.exercise = exercise
        self.split = split
        self.distance = distance
        self.metric = metric
        self.circuit = circuit
        self.order_in_circuit = order_in_circuit
        self.notes = notes
        self.circuit_count = circuit_count
        self.exercise_count = exercise_count
        self.user_id = user_id
        self.sub_id = sub_id
    
    # functions
    