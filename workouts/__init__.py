#workouts/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
# import config # removed for deployment

app = Flask(__name__)

def configure():
    load_dotenv()

# app.config['SECRET_KEY'] = config.get_secret_key() # changed for deployment
app.config['SECRET_KEY'] = os.getenv('secret_key')

### database setup ###
# app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_url() # changed for deployment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('sqlalchemy_database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
### database setup ###

### login manager ###
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
### login manager ###

### blueprint registrations ###
from workouts.core.views import core
from workouts.error_pages.handlers import error_pages
from workouts.users.views import users
from workouts.strength_training_sub.views import strength_training_sub
from workouts.strength_training.views import strength_training
from workouts.cardio_training.views import cardio_training
from workouts.cardio_training_sub.views import cardio_training_sub
from workouts.recovery_questions.views import recovery_questions
from workouts.aggregate.views import aggregate
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(strength_training_sub)
app.register_blueprint(strength_training)
app.register_blueprint(cardio_training_sub)
app.register_blueprint(cardio_training)
app.register_blueprint(recovery_questions)
app.register_blueprint(aggregate)
### blueprint registrations ###
