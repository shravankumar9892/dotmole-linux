from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('pages/placeholder.dashboard.html')

@app.route('/dashboard/activity')
def dashboard_activity():
    return render_template('pages/placeholder.dashboard_activity.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/snitcher/add')
def addnew():
    return render_template('pages/placeholder.snitcheradd.html')

@app.route('/snitcher/view/configurations')
def viewconfig():
    return render_template('pages/placeholder.viewconfig.html')

@app.route('/snitcher/view/messages')
def viewnew():
    return render_template('pages/placeholder.snitcherview.html')

@app.route('/contact')
def contact():
    return render_template('pages/placeholder.contact.html')

@app.route('/login')
def login():
    return render_template('forms/login.html')


@app.route('/register')
def register():
    return render_template('forms/register.html')

@app.route('/profile')
def profile():
    return render_template('pages/placeholder.profile.html')

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
