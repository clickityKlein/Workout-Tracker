#cardio_training/views.py
from flask import render_template, redirect, url_for, request, Blueprint, flash
from workouts import db
from flask_login import current_user, login_required
from workouts.models import CardioTraining, CardioTrainingSub, User
from workouts.cardio_training.forms import CardioTrainingForm, UpdateCardioTrainingForm

cardio_training = Blueprint('cardio_training', __name__)

# create
@cardio_training.route('/create_cardio_workout', methods=['GET', 'POST'])
@login_required
def create_cardio_workout():
    form = CardioTrainingForm()
    sub_form_parameters = CardioTrainingSub.query.filter_by(user_id=current_user.id).order_by(CardioTrainingSub.id.desc()).first()
    
    '''
    IMPORTANT NOTE:
    - DO NOT USE "field = form.field.data" wtforms method
    - USE html manual form creation and dynamic naming
    '''
    # time validation
    def validate_time_input(field):
        try:
            hours, minutes, seconds = map(int, field.split(':'))
            if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
                return True
        
            else:
                return False
        
        except ValueError:
            return False
    
    # ensure athlete is user
    if sub_form_parameters.athlete != current_user:
        abort(403)
    
    
    if form.validate_on_submit():
        for circuit_row in range(sub_form_parameters.circuit_count):
            for exercise_row in range(sub_form_parameters.exercise_count):
                split = request.form.get(f'split_{circuit_row}_{exercise_row}')
                if not validate_time_input(split):
                    flash("Invalid Split Format, must be HH:MM:SS", "error")
                    return redirect(url_for('cardio_training.create_cardio_workout'))
                
    
    if form.validate_on_submit():
        for circuit_row in range(sub_form_parameters.circuit_count):
            for exercise_row in range(sub_form_parameters.exercise_count):
                
                workout_name = sub_form_parameters.workout_name
                date = sub_form_parameters.date
                location = sub_form_parameters.location
                exercise = request.form.get(f'exercise_{circuit_row}_{exercise_row}')
                split = request.form.get(f'split_{circuit_row}_{exercise_row}')
                distance = request.form.get(f'distance_{circuit_row}_{exercise_row}')
                metric = request.form.get(f'metric_{circuit_row}_{exercise_row}')
                circuit = request.form.get(f'circuit_{circuit_row}_{exercise_row}')
                order_in_circuit = request.form.get(f'order_in_circuit_{circuit_row}_{exercise_row}')
                notes = request.form.get(f'notes_{circuit_row}_{exercise_row}')
                exercise_count = sub_form_parameters.exercise_count
                circuit_count = sub_form_parameters.circuit_count
                user_id = sub_form_parameters.user_id
                sub_id = sub_form_parameters.id
    
                cardio_workout = CardioTraining(workout_name=workout_name,
                                                date=date,
                                                location=location,
                                                exercise=exercise,
                                                split=split,
                                                distance=distance,
                                                metric=metric,
                                                circuit=circuit,
                                                order_in_circuit=order_in_circuit,
                                                notes=notes,
                                                exercise_count=exercise_count,
                                                circuit_count=circuit_count,
                                                user_id=user_id,
                                                sub_id=sub_id)
                
                db.session.add(cardio_workout)
                db.session.commit()
    
        return redirect(url_for('core.index'))
    
    else:
        print(f'\n{form.errors}\n')
    
    return render_template('create_cardio_workout.html',
                           form=form,
                           workout_name=sub_form_parameters.workout_name,
                           date=sub_form_parameters.date,
                           location=sub_form_parameters.location,
                           exercise_count=sub_form_parameters.exercise_count,
                           circuit_count=sub_form_parameters.circuit_count)


# read (table workout view)
@cardio_training.route('/track_cardio_workouts/<int:cardio_user_id>', methods=['GET', 'POST'])
@login_required
def view_cardio_workout_table(cardio_user_id):
    
    cardio_training_data = CardioTraining.query.filter_by(user_id=cardio_user_id)
    
    table_username = User.query.filter_by(id=cardio_user_id).first().username
        
    return render_template('track_cardio_workouts.html',
                           cardio_training_data=cardio_training_data,
                           table_username=table_username)


# read (single view)
# "int:" treats as integer
@cardio_training.route('/view_single_cardio_workout/<int:cardio_workout_id>/<int:cardio_user_id>')
def single_cardio_workout(cardio_workout_id, cardio_user_id):
    cardio_workout = CardioTraining.query.filter_by(sub_id=cardio_workout_id).filter_by(user_id=cardio_user_id).all()
    
    table_username = User.query.filter_by(id=cardio_user_id).first().username
    
    enable_edit = cardio_workout[0].user_id == current_user.id
    
    return render_template('view_single_cardio_workout.html',
                           cardio_workout=cardio_workout,
                           enable_edit=enable_edit,
                           table_username=table_username)


# delete
@cardio_training.route('/<int:cardio_workout_id>/delete_cardio', methods=['GET', 'POST'])
@login_required
def delete_cardio_workout(cardio_workout_id):
    main_cardio_workout = CardioTraining.query.filter_by(sub_id=cardio_workout_id).filter_by(user_id=current_user.id).all()
    sub_cardio_workout = CardioTrainingSub.query.filter_by(id=cardio_workout_id).filter_by(user_id=current_user.id).all()
    
    if main_cardio_workout:
        for workout in main_cardio_workout:
            db.session.delete(workout)
    
    if sub_cardio_workout:
        for workout in sub_cardio_workout:
            db.session.delete(workout)
    
    db.session.commit()
    
    return redirect(url_for('cardio_training.view_cardio_workout_table', cardio_user_id=current_user.id))


# update
@cardio_training.route('/<int:cardio_workout_id>/update_cardio', methods=['GET', 'POST'])
@login_required
def update_cardio_workout(cardio_workout_id):
    form = UpdateCardioTrainingForm()
    selected_workout = CardioTraining.query.filter_by(user_id=current_user.id).filter_by(sub_id=cardio_workout_id).all()
    selected_sub_workout = CardioTrainingSub.query.filter_by(user_id=current_user.id).filter_by(id=cardio_workout_id).first()
    
    '''
    IMPORTANT NOTE:
    - DO NOT USE "field = form.field.data" wtforms method
    - USE html manual form creation and dynamic naming
    '''
    
    # the workout should exist, but in the event that it does not
    if selected_workout is None:
        flash('Workout Does Not Exist!')
        return redirect(url_for('cardio_training.view_cardio_workout_table', cardio_user_id=current_user.id))
        
    # ensure athlete is user
    if selected_workout[0].user_id != current_user.id:
        abort(403)
        
    # constants
    workout_name = selected_workout[0].workout_name
    date = selected_workout[0].date
    location = selected_workout[0].location
    exercise_count = selected_workout[0].exercise_count
    circuit_count = selected_workout[0].circuit_count
    
    # initial storage
    exercise_list = []
    split_list = []
    distance_list = []
    metric_list = []
    circuit_list = []
    order_in_circuit_list = []
    notes_list = []
    
    # results storage
    results_exercise_list = []
    results_split_list = []
    results_distance_list = []
    results_metric_list = []
    results_circuit_list = []
    results_order_in_circuit_list = []
    results_notes_list = []
    
    if request.method == 'GET':
        
        for set_row in selected_workout:
                exercise_list.append(set_row.exercise)
                split_list.append(set_row.split)
                distance_list.append(set_row.distance)
                metric_list.append(set_row.metric)
                circuit_list.append(set_row.circuit)
                order_in_circuit_list.append(set_row.order_in_circuit)
                notes_list.append(set_row.notes)
                
            
    elif request.method == 'POST':
            
        # constants
        workout_name = form.workout_name.data
        date = form.date.data
        location = form.location.data
        
        # update sub workout
        selected_sub_workout.workout_name = workout_name
        selected_sub_workout.date = date
        selected_sub_workout.location = location
        
        for circuit_row in range(circuit_count):
            for exercise_row in range(exercise_count):
                
                results_exercise_list.append(request.form.get(f'exercise_{circuit_row}_{exercise_row}'))
                results_split_list.append(request.form.get(f'split_{circuit_row}_{exercise_row}'))
                results_distance_list.append(request.form.get(f'distance_{circuit_row}_{exercise_row}'))
                results_metric_list.append(request.form.get(f'metric_{circuit_row}_{exercise_row}'))
                results_circuit_list.append(request.form.get(f'circuit_{circuit_row}_{exercise_row}'))
                results_order_in_circuit_list.append(request.form.get(f'order_in_circuit_{circuit_row}_{exercise_row}'))
                results_notes_list.append(request.form.get(f'notes_{circuit_row}_{exercise_row}'))       
        
        # update workout
        for num, set_row in enumerate(selected_workout):
            
            set_row.exercise = results_exercise_list[num]
            set_row.split = results_split_list[num]
            set_row.distance = results_distance_list[num]
            set_row.metric = results_metric_list[num]
            set_row.circuit = results_circuit_list[num]
            set_row.order_in_circuit = results_order_in_circuit_list[num]
            set_row.notes = results_notes_list[num]
            
        db.session.commit()
        
        return redirect(url_for('cardio_training.single_cardio_workout',
                                cardio_workout_id=cardio_workout_id,
                                cardio_user_id=current_user.id))
    
    return render_template('update_cardio_workout.html',
                           form=form,
                           workout_name=workout_name,
                           date=date,
                           location=location,
                           exercise_count=exercise_count,
                           circuit_count=circuit_count,
                           exercise_list=exercise_list,
                           split_list=split_list,
                           distance_list=distance_list,
                           metric_list=metric_list,
                           circuit_list=circuit_list,
                           order_in_circuit_list=order_in_circuit_list,
                           notes_list=notes_list)
