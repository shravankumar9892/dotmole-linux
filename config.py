import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Connects to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Enable debug mode.
    DEBUG = True
    FLASK_ENV='development'
    TEMPLATES_AUTO_RELOAD = True
    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'my precious'