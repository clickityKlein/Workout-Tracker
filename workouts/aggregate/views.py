#cardio_training/views.py
from flask import render_template, redirect, url_for, request, Blueprint, flash
from workouts import db
from flask_login import current_user, login_required
from workouts.models import CardioTraining, CardioTrainingSub, StrengthTraining, StrengthTrainingSub
import pandas as pd
from werkzeug.wrappers import Response
from sqlalchemy import select


aggregate = Blueprint('aggregate', __name__)


# read (summarized table strength workout view)
@aggregate.route('/aggregate_strength_summary', methods=['GET', 'POST'])
@login_required
def summarized_strength_workout_table():
    # only need faux cleaner for showing summarized results
    strength_training_data = StrengthTrainingSub.query.where(StrengthTrainingSub.id==StrengthTraining.sub_id).all()
    
    return render_template('aggregate_strength_summary.html',
                           strength_training_data=strength_training_data)


# read (summarized table cardio workout view)
@aggregate.route('/aggregate_cardio_summary', methods=['GET', 'POST'])
@login_required
def summarized_cardio_workout_table():
    # only need faux cleaner for showing summarized results
    cardio_training_data = CardioTrainingSub.query.where(CardioTrainingSub.id==CardioTraining.sub_id).all()
        
    return render_template('aggregate_cardio_summary.html',
                           cardio_training_data=cardio_training_data)


# read (detailed table strength workout view)
@aggregate.route('/aggregate_strength_detailed', methods=['GET', 'POST'])
@login_required
def detailed_strength_workout_table():
    # only need faux cleaner for showing summarized results
    strength_training_data = StrengthTraining.query.all()
        
    return render_template('aggregate_strength_detailed.html',
                           strength_training_data=strength_training_data)


# read (detailed table cardio workout view)
@aggregate.route('/aggregate_cardio_detailed', methods=['GET', 'POST'])
@login_required
def detailed_cardio_workout_table():
    # only need faux cleaner for showing summarized results
    cardio_training_data = CardioTraining.query.all()
        
    return render_template('aggregate_cardio_detailed.html',
                           cardio_training_data=cardio_training_data)


# export strength workouts
@aggregate.route('/export_aggregate_strength', methods=['GET', 'POST'])
def export_aggregate_strength_workouts():
    
    strength_training_data = StrengthTraining.query.all()
    strength_cols = ['user_id', 'workout_name', 'date', 'location', 'exercise', 'weight',
                     'metric', 'repetitions', 'set_number', 'order_in_set', 'notes']
    
    strength_dict = {col:[] for col in strength_cols}
    for record in strength_training_data:
        for col in strength_cols:
            strength_dict[col].append(eval(f'record.{col}'))
    
    df = pd.DataFrame(strength_dict)
    filename = "strength_workouts_aggregate.csv"
    df.to_csv(filename, index=True)
    
    download_file = Response(open(filename, 'rb'), mimetype='text/csv')
    download_file.headers.set("Content-Disposition", "attachment", filename=filename)
    
    return download_file


# export cardio workouts
@aggregate.route('/export_aggregate_cardio', methods=['GET', 'POST'])
def export_aggregate_cardio_workouts():
    
    cardio_training_data = CardioTraining.query.all()
    cardio_cols = ['user_id', 'workout_name', 'date', 'location', 'exercise', 'split',
                   'distance', 'metric', 'circuit', 'order_in_circuit', 'notes']
    
    cardio_dict = {col:[] for col in cardio_cols}
    for record in cardio_training_data:
        for col in cardio_cols:
            cardio_dict[col].append(eval(f'record.{col}'))
    
    df = pd.DataFrame(cardio_dict)
    filename = "cardio_workouts_aggregate.csv"
    df.to_csv(filename, index=True)
    
    download_file = Response(open(filename, 'rb'), mimetype='text/csv')
    download_file.headers.set("Content-Disposition", "attachment", filename=filename)
    
    return download_file
