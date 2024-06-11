#cardio_training_sub/views.py
from flask import render_template, redirect, url_for, request, Blueprint
from workouts import db
from flask_login import current_user, login_required
from workouts.models import CardioTrainingSub, CardioTraining, User
from workouts.cardio_training_sub.forms import CardioTrainingSubForm

cardio_training_sub = Blueprint('cardio_training_sub', __name__)

# create
@cardio_training_sub.route('/create_cardio_workout_sub', methods=['GET', 'POST'])
@login_required
def create_cardio_workout_sub():
    form = CardioTrainingSubForm()
    if form.validate_on_submit():
        cardio_workout_sub = CardioTrainingSub(workout_name=form.workout_name.data,
                                               date=form.date.data,
                                               location=form.location.data,
                                               exercise_count=form.exercise_count.data,
                                               circuit_count=form.circuit_count.data,
                                               user_id=current_user.id)
        db.session.add(cardio_workout_sub)
        db.session.commit()
        return redirect(url_for('cardio_training.create_cardio_workout'))
    return render_template('create_cardio_workout_sub.html', form=form)


# read (table workout view)
@cardio_training_sub.route('/track_cardio_sub_workouts/<int:cardio_user_id>', methods=['GET', 'POST'])
@login_required
def view_cardio_sub_workout_table(cardio_user_id):
    # only need faux cleaner for showing summarized results
    cardio_sub_training_data = CardioTrainingSub.query.filter_by(user_id=cardio_user_id).where(CardioTrainingSub.id==CardioTraining.sub_id)
    table_username = User.query.filter_by(id=cardio_user_id).first().username
    
    return render_template('track_cardio_sub_workouts.html',
                           cardio_sub_training_data=cardio_sub_training_data,
                           table_username=table_username)
