#strength_training/views.py
from flask import render_template, redirect, url_for, request, Blueprint, flash
from workouts import db
from flask_login import current_user, login_required
from workouts.models import StrengthTraining, StrengthTrainingSub, User
from workouts.strength_training.forms import StrengthTrainingForm, UpdateStrengthTrainingForm


strength_training = Blueprint('strength_training', __name__)


# create
@strength_training.route('/create_strength_workout', methods=['GET', 'POST'])
@login_required
def create_strength_workout():
    form = StrengthTrainingForm()
    sub_form_parameters = StrengthTrainingSub.query.filter_by(user_id=current_user.id).order_by(StrengthTrainingSub.id.desc()).first()
    
    '''
    IMPORTANT NOTE:
    - DO NOT USE "field = form.field.data" wtforms method
    - USE html manual form creation and dynamic naming
    '''
    
    # ensure athlete is user
    if sub_form_parameters.athlete != current_user:
        abort(403)
    
    if form.validate_on_submit():
        for set_row in range(sub_form_parameters.set_count):
            for exercise_row in range(sub_form_parameters.exercise_count):
                
                workout_name = sub_form_parameters.workout_name
                date = sub_form_parameters.date
                location = sub_form_parameters.location
                exercise = request.form.get(f'exercise_{set_row}_{exercise_row}')
                weight = request.form.get(f'weight_{set_row}_{exercise_row}')
                metric = request.form.get(f'metric_{set_row}_{exercise_row}')
                repetitions = request.form.get(f'repetitions_{set_row}_{exercise_row}')
                set_number = request.form.get(f'set_number_{set_row}_{exercise_row}')
                order_in_set = request.form.get(f'order_in_set_{set_row}_{exercise_row}')
                notes = request.form.get(f'notes_{set_row}_{exercise_row}')
                exercise_count = sub_form_parameters.exercise_count
                set_count = sub_form_parameters.set_count
                user_id = sub_form_parameters.user_id
                sub_id = sub_form_parameters.id
    
                strength_workout = StrengthTraining(workout_name=workout_name,
                                                  date=date,
                                                  location=location,
                                                  exercise=exercise,
                                                  weight=weight,
                                                  metric=metric,
                                                  repetitions=repetitions,
                                                  set_number=set_number,
                                                  order_in_set=order_in_set,
                                                  notes=notes,
                                                  exercise_count=exercise_count,
                                                  set_count=set_count,
                                                  user_id=user_id,
                                                  sub_id=sub_id)
                
                db.session.add(strength_workout)
                db.session.commit()

        return redirect(url_for('core.index'))
    
    else:
        print(f'\n{form.errors}\n')
    
    return render_template('create_strength_workout.html',
                           form=form,
                           workout_name=sub_form_parameters.workout_name,
                           date=sub_form_parameters.date,
                           location=sub_form_parameters.location,
                           exercise_count=sub_form_parameters.exercise_count,
                           set_count=sub_form_parameters.set_count)


# read (table workout view)
@strength_training.route('/track_strength_workouts/<int:strength_user_id>', methods=['GET', 'POST'])
@login_required
def view_strength_workout_table(strength_user_id):
    strength_training_data = StrengthTraining.query.filter_by(user_id=strength_user_id)
    
    table_username = User.query.filter_by(id=strength_user_id).first().username
    
    return render_template('track_strength_workouts.html',
                           strength_training_data=strength_training_data,
                           table_username=table_username)


# read (single view)
# "int:" treats as integer
@strength_training.route('/view_single_strength_workout/<int:strength_workout_id>/<int:strength_user_id>')
def single_strength_workout(strength_workout_id, strength_user_id):
    strength_workout = StrengthTraining.query.filter_by(sub_id=strength_workout_id).filter_by(user_id=strength_user_id).all()

    table_username = User.query.filter_by(id=strength_user_id).first().username

    enable_edit = strength_workout[0].user_id == current_user.id
    
    return render_template('view_single_strength_workout.html',
                           strength_workout=strength_workout,
                           enable_edit=enable_edit,
                           table_username=table_username)


# delete
@strength_training.route('/<int:strength_workout_id>/delete_strength', methods=['GET', 'POST'])
@login_required
def delete_strength_workout(strength_workout_id):
    main_strength_workout = StrengthTraining.query.filter_by(sub_id=strength_workout_id).filter_by(user_id=current_user.id).all()
    sub_strength_workout = StrengthTrainingSub.query.filter_by(id=strength_workout_id).filter_by(user_id=current_user.id).all()
    
    if main_strength_workout:
        for workout in main_strength_workout:
            db.session.delete(workout)
    
    if sub_strength_workout:
        for workout in sub_strength_workout:
            db.session.delete(workout)
    
    db.session.commit()
    
    return redirect(url_for('strength_training.view_strength_workout_table', strength_user_id=current_user.id))


# update
@strength_training.route('/<int:strength_workout_id>/update_strength', methods=['GET', 'POST'])
@login_required
def update_strength_workout(strength_workout_id):
    form = UpdateStrengthTrainingForm()
    selected_workout = StrengthTraining.query.filter_by(user_id=current_user.id).filter_by(sub_id=strength_workout_id).all()
    selected_sub_workout = StrengthTrainingSub.query.filter_by(user_id=current_user.id).filter_by(id=strength_workout_id).first()
    
    '''
    IMPORTANT NOTE:
    - DO NOT USE "field = form.field.data" wtforms method
    - USE html manual form creation and dynamic naming
    '''
    
    # the workout should exist, but in the event that it does not
    if selected_workout is None:
        flash('Workout Does Not Exist!')
        return redirect(url_for('strength_training.view_strength_workout_table', strength_user_id=current_user.id))
        
    # ensure athlete is user
    if selected_workout[0].user_id != current_user.id:
        abort(403)
        
    # constants
    workout_name = selected_workout[0].workout_name
    date = selected_workout[0].date
    location = selected_workout[0].location
    exercise_count = selected_workout[0].exercise_count
    set_count = selected_workout[0].set_count
    
    # initial storage
    exercise_list = []
    weight_list = []
    metric_list = []
    repetitions_list = []
    set_number_list = []
    order_in_set_list = []
    notes_list = []
    
    # results storage
    results_exercise_list = []
    results_weight_list = []
    results_metric_list = []
    results_repetitions_list = []
    results_set_number_list = []
    results_order_in_set_list = []
    results_notes_list = []
    
    if request.method == 'GET':
        
        for set_row in selected_workout:
                exercise_list.append(set_row.exercise)
                weight_list.append(set_row.weight)
                metric_list.append(set_row.metric)
                repetitions_list.append(set_row.repetitions)
                set_number_list.append(set_row.set_number)
                order_in_set_list.append(set_row.order_in_set)
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
        
        for set_row in range(set_count):
            for exercise_row in range(exercise_count):
                
                results_exercise_list.append(request.form.get(f'exercise_{set_row}_{exercise_row}'))
                results_weight_list.append(request.form.get(f'weight_{set_row}_{exercise_row}'))
                results_metric_list.append(request.form.get(f'metric_{set_row}_{exercise_row}'))
                results_repetitions_list.append(request.form.get(f'repetitions_{set_row}_{exercise_row}'))
                results_set_number_list.append(request.form.get(f'set_number_{set_row}_{exercise_row}'))
                results_order_in_set_list.append(request.form.get(f'order_in_set_{set_row}_{exercise_row}'))
                results_notes_list.append(request.form.get(f'notes_{set_row}_{exercise_row}'))       
        
        # update workout
        for num, set_row in enumerate(selected_workout):
            
            set_row.exercise = results_exercise_list[num]
            set_row.weight = results_weight_list[num]
            set_row.metric = results_metric_list[num]
            set_row.repetitions = results_repetitions_list[num]
            set_row.set_num = results_set_number_list[num]
            set_row.order_in_set = results_order_in_set_list[num]
            set_row.notes = results_notes_list[num]
            
        db.session.commit()
        
        return redirect(url_for('strength_training.single_strength_workout',
                                strength_workout_id=strength_workout_id,
                                strength_user_id=current_user.id))
    
    return render_template('update_strength_workout.html',
                           form=form,
                           workout_name=workout_name,
                           date=date,
                           location=location,
                           exercise_count=exercise_count,
                           set_count=set_count,
                           exercise_list=exercise_list,
                           weight_list=weight_list,
                           metric_list=metric_list,
                           repetitions_list=repetitions_list,
                           set_number_list=set_number_list,
                           order_in_set_list=order_in_set_list,
                           notes_list=notes_list)
