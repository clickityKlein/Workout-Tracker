#users/views.py
from flask import render_template, redirect, url_for, request, Blueprint, render_template_string, flash
from flask_login import login_user, current_user, logout_user, login_required
from workouts import db
from workouts.models import User, StrengthTraining, StrengthTrainingSub, CardioTraining, CardioTrainingSub, RecoveryQuestions
from workouts.users.forms import RegistrationForm, LoginForm, UpdateUserForm
import pandas as pd
from werkzeug.wrappers import Response
from sqlalchemy import select


users = Blueprint('users', __name__)


# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    
    def check_email(entered_email):
        if User.query.filter_by(email=entered_email).first() is not None:
            flash('This email has been registered previously.')
            return False
        else:
            return True
            
    def check_username(entered_username):
        if User.query.filter_by(username=entered_username).first() is not None:
            flash('This username is not available.')
            return False
        else:
            return True
        
    if form.validate_on_submit():
        if check_email(form.email.data) and check_username(form.username.data):
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.login'))
        else:
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)


# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("No Account Associated With That Email!")
            return redirect(url_for('users.login'))
        elif not user.check_password(form.password.data):
            flash("Incorrect Password!")
            return redirect(url_for('users.login'))
        elif user is not None and user.check_password(form.password.data):
            login_user(user)
            clean_workouts()
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
        else:
            return redirect(url_for('core.index'))
        
    return render_template('login.html', form=form)
            

# logout
@users.route('/logout')
def logout():
    clean_workouts()
    logout_user()
    return redirect(url_for('core.index'))


# account
@users.route('/account', methods=['GET', 'POST'])
def account():
    recovery_questions = RecoveryQuestions.query.filter_by(user_id=current_user.id).first()
    if recovery_questions is not None:
        recovery_questions_set = True
    else:
        recovery_questions_set = False
        flash('Please Update Recovery Questions! It Is The Only Way To Recover Your Account!')
    
    form = UpdateUserForm()
    
    if request.method == 'POST':
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Information Updated!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('account.html', form=form, recovery_questions_set=recovery_questions_set)


# export strength workouts
@users.route('/export_strength', methods=['GET', 'POST'])
def export_strength_workouts():
    
    strength_training_data = StrengthTraining.query.filter_by(user_id=current_user.id).order_by(StrengthTraining.id.desc()).all()
    strength_cols = ['workout_name', 'date', 'location', 'exercise', 'weight',
                     'metric', 'repetitions', 'set_number', 'order_in_set', 'notes']
    
    strength_dict = {col:[] for col in strength_cols}
    for record in strength_training_data:
        for col in strength_cols:
            strength_dict[col].append(eval(f'record.{col}'))
    
    df = pd.DataFrame(strength_dict)
    filename = f"strength_workouts_{current_user.username}.csv"
    df.to_csv(filename, index=True)
    
    download_file = Response(open(filename, 'rb'), mimetype='text/csv')
    # download_file.headers.set("Content-Disposition", "attachment", filename=filename)
    download_file.headers.set("Content-Disposition", f"attachment; filename={filename}")
    
    return download_file

# export cardio workouts
@users.route('/export_cardio', methods=['GET', 'POST'])
def export_cardio_workouts():
    
    cardio_training_data = CardioTraining.query.filter_by(user_id=current_user.id).order_by(CardioTraining.id.desc()).all()
    cardio_cols = ['workout_name', 'date', 'location', 'exercise', 'split', 'distance',
                     'metric', 'circuit', 'order_in_circuit', 'notes']
    
    cardio_dict = {col:[] for col in cardio_cols}
    for record in cardio_training_data:
        for col in cardio_cols:
            cardio_dict[col].append(eval(f'record.{col}'))
    
    df = pd.DataFrame(cardio_dict)
    filename = f"cardio_workouts_{current_user.username}.csv"
    df.to_csv(filename, index=True)
    
    download_file = Response(open(filename, 'rb'), mimetype='text/csv')
    download_file.headers.set("Content-Disposition", f"attachment; filename={filename}")
    
    return download_file


# sub strength cleaner - because we didn't use event manager, we can have more sub workouts than unique workouts
# delete
@users.route('/cleaner', methods=['GET', 'POST'])
@login_required
def clean_workouts():
    # get strength workouts
    main_strength_workouts = StrengthTraining.query.filter_by(user_id=current_user.id).all()
    sub_strength_workouts = StrengthTrainingSub.query.filter_by(user_id=current_user.id).all()
    
    # get cardio workouts
    main_cardio_workouts = CardioTraining.query.filter_by(user_id=current_user.id).all()
    sub_cardio_workouts = CardioTrainingSub.query.filter_by(user_id=current_user.id).all()
    
    # strength cleaner
    if main_strength_workouts:
        main_workout_set = set()
        for workout in main_strength_workouts:
            main_workout_set.add(workout.sub_id)
    
    if sub_strength_workouts:
        sub_workout_set = set()
        for workout in sub_strength_workouts:
            sub_workout_set.add(workout.id)
            
    remove_workouts_set = sub_workout_set.difference(main_workout_set)
    if len(remove_workouts_set) > 0:
        for workout in remove_workouts_set:
            remove_workout = StrengthTrainingSub.query.filter_by(user_id=current_user.id).filter_by(id=workout).all()
            for remove_query in remove_workout:
                db.session.delete(remove_query)
                
    # cardio cleaner
    if main_cardio_workouts:
        main_workout_set = set()
        for workout in main_cardio_workouts:
            main_workout_set.add(workout.sub_id)
    
    if sub_cardio_workouts:
        sub_workout_set = set()
        for workout in sub_cardio_workouts:
            sub_workout_set.add(workout.id)
            
    remove_workouts_set = sub_workout_set.difference(main_workout_set)
    if len(remove_workouts_set) > 0:
        for workout in remove_workouts_set:
            remove_workout = CardioTrainingSub.query.filter_by(user_id=current_user.id).filter_by(id=workout).all()
            for remove_query in remove_workout:
                db.session.delete(remove_query)
    
    db.session.commit()
