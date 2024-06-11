#users/views.py
from flask import render_template, redirect, url_for, request, Blueprint, render_template_string, flash
from flask_login import login_user, current_user, logout_user, login_required
from workouts import db
from workouts.models import User, RecoveryQuestions
from workouts.recovery_questions.forms import SetRecoveryQuestionsForm, ResetRecoveryQuestionsForm, AnswerRecoveryQuestionsForm, StartRecoveryQuestionsForm


recovery_questions = Blueprint('recovery_questions', __name__)


# set recovery questions
@recovery_questions.route('/set_recovery_questions', methods=['GET', 'POST'])
def set_recovery_questions():
    # flash("Please Select Unique Questions.")
    form = SetRecoveryQuestionsForm()
    
    # unique question validation
    def validate_unique_questions():
        try:
            question_selection = [form.question_1.data,
                                  form.question_2.data,
                                  form.question_3.data,
                                  form.question_4.data,
                                  form.question_5.data]
            if len(set(question_selection)) == 5:
                return True
        
            else:
                return False
        
        except ValueError:
            return False
    
    
    if form.validate_on_submit():
        print('\n success \n')
        if not validate_unique_questions():
            flash("All Recovery Questions Must Be Unique. Please Select Unique Questions.", "error")
            # return render_template('set_recovery_questions.html', form=form)
        else:
            recovery_questions = RecoveryQuestions(question_1=form.question_1.data,
                                                   answer_1=form.answer_1.data,
                                                   question_2=form.question_2.data,
                                                   answer_2=form.answer_2.data,
                                                   question_3=form.question_3.data,
                                                   answer_3=form.answer_3.data,
                                                   question_4=form.question_4.data,
                                                   answer_4=form.answer_4.data,
                                                   question_5=form.question_5.data,
                                                   answer_5=form.answer_5.data,
                                                   user_id=current_user.id)
        
            db.session.add(recovery_questions)
            db.session.commit()
            return redirect(url_for('users.account'))
    else:
        print(f'\n\n{form.errors}\n\n')
    
    return render_template('set_recovery_questions.html', form=form)

# view
@recovery_questions.route('/reset_recovery_questions', methods=['GET', 'POST'])
@login_required
def reset_recovery_questions():
    current_responses = RecoveryQuestions.query.filter_by(user_id=current_user.id).first()
    form = ResetRecoveryQuestionsForm()
    if request.method == "POST":
        current_responses.question_1 = form.question_1.data
        current_responses.question_2 = form.question_2.data
        current_responses.question_3 = form.question_3.data
        current_responses.question_4 = form.question_4.data
        current_responses.question_5 = form.question_5.data
        
        current_responses.answer_1 = form.answer_1.data
        current_responses.answer_2 = form.answer_2.data
        current_responses.answer_3 = form.answer_3.data
        current_responses.answer_4 = form.answer_4.data
        current_responses.answer_5 = form.answer_5.data
        
        db.session.commit()
        flash('Recovery Questions Updated!')
        return redirect(url_for('users.account'))
        
    elif request.method == "GET":
        form.question_1.data = current_responses.question_1
        form.question_2.data = current_responses.question_2
        form.question_3.data = current_responses.question_3
        form.question_4.data = current_responses.question_4
        form.question_5.data = current_responses.question_5
    

    return render_template('reset_recovery_questions.html', form=form)


@recovery_questions.route('/start_recovery_questions', methods=['GET', 'POST'])
def start_recovery_questions():
    form = StartRecoveryQuestionsForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        try_email = form.email.data
        # print(f'\n\n\n  {try_email} \n\n\n')
        return redirect(url_for('recovery_questions.answer_recovery_questions', try_email=try_email))
    
    return render_template('start_recovery_questions.html', form=form)

# answer recovery questions - i.e. recover account
@recovery_questions.route('/answer_recovery_questions/<try_email>', methods=['GET', 'POST'])
def answer_recovery_questions(try_email):
    question_choices = [(1, "What’s the name of your parent’s pet?"),
                        (2, "What's the name of your first pet?"),
                        (3, "What's the name of your favorite book?"),
                        (4, "What's the name of your childhood best friend?"),
                        (5, "What city were you born in?"),
                        (6, "What's your favorite color?"),
                        (7, "What's the make and model of your first car?"),
                        (8, "What's the name of your high school mascot?"),
                        (9, "What's your favorite food?"),
                        (10, "What's the name of your favorite teacher?"),
                        (11, "What was your nickname?"),
                        (12, "What's your favorite hobby?")]

    form = AnswerRecoveryQuestionsForm()
    user = User.query.filter_by(email=try_email).first()
    if user is not None:
        saved_responses = RecoveryQuestions.query.filter_by(user_id=user.id).first()
        if saved_responses is None:
            flash("Recovery Questions Not Present For This Account!")
            return redirect(url_for('recovery_questions.start_recovery_questions'))
    else:
        flash("No Account Associated With That Email!")
        return redirect(url_for('recovery_questions.start_recovery_questions'))
    
    question_1 = saved_responses.question_1
    question_2 = saved_responses.question_2
    question_3 = saved_responses.question_3
    question_4 = saved_responses.question_4
    question_5 = saved_responses.question_5
    
    if form.validate_on_submit():
        
        response_1 = saved_responses.check_answer_1(form.answer_1.data)
        response_2 = saved_responses.check_answer_2(form.answer_2.data)
        response_3 = saved_responses.check_answer_3(form.answer_3.data)
        response_4 = saved_responses.check_answer_4(form.answer_4.data)
        response_5 = saved_responses.check_answer_5(form.answer_5.data)
        
        try_responses = [response_1, response_2, response_3, response_4, response_5]
        
        if sum(try_responses) > 1:
            login_user(user)
            flash("Account Recovered, Please Reset Password!")
            return redirect(url_for('users.account'))
        else:
            flash("Please Answer At Least 2 Questions Correctly!")
        
        
    else:
        print(f'\n\n\n {form.errors} \n\n\n')
    
    return render_template('answer_recovery_questions.html',
                           form=form,
                           question_1=question_1,
                           question_2=question_2,
                           question_3=question_3,
                           question_4=question_4,
                           question_5=question_5,
                           question_choices=question_choices)

