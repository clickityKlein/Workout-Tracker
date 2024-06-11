#strength_training_sub/views.py
from flask import render_template, redirect, url_for, request, Blueprint
from workouts import db
from flask_login import current_user, login_required
from workouts.models import StrengthTrainingSub, StrengthTraining, User
from workouts.strength_training_sub.forms import StrengthTrainingSubForm

strength_training_sub = Blueprint('strength_training_sub', __name__)

# create
@strength_training_sub.route('/create_strength_workout_sub', methods=['GET', 'POST'])
@login_required
def create_strength_workout_sub():
    form = StrengthTrainingSubForm()
    if form.validate_on_submit():
        print('form validation successful')
        strength_workout_sub = StrengthTrainingSub(workout_name=form.workout_name.data,
                                                   date=form.date.data,
                                                   location=form.location.data,
                                                   exercise_count=form.exercise_count.data,
                                                   set_count=form.set_count.data,
                                                   user_id=current_user.id)
        db.session.add(strength_workout_sub)
        db.session.commit()
        return redirect(url_for('strength_training.create_strength_workout'))

    return render_template('create_strength_workout_sub.html', form=form)


# read (table workout view)
@strength_training_sub.route('/track_strength_sub_workouts/<int:strength_user_id>', methods=['GET', 'POST'])
@login_required
def view_strength_sub_workout_table(strength_user_id):
    # only need faux cleaner for showing summarized results
    strength_sub_training_data = StrengthTrainingSub.query.filter_by(user_id=strength_user_id).where(StrengthTrainingSub.id==StrengthTraining.sub_id)
    
    table_username = User.query.filter_by(id=strength_user_id).first().username
    
    return render_template('track_strength_sub_workouts.html',
                           strength_sub_training_data=strength_sub_training_data,
                           table_username=table_username)
