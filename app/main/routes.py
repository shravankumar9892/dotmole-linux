import datetime
import glob
import os
import shutil
import subprocess
import time
import threading
import urllib.request

import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
from flask import (Response, jsonify, redirect, render_template, request,
                   stream_with_context, url_for, flash)
from app.models import Configuration
from flask_login import current_user, login_required
from mtcnn.mtcnn import MTCNN
from pyfacy import face_clust  # use for face clustering
from werkzeug.utils import secure_filename

from app import db
from app.main import bp, settings
from app.main.forms import ConfigurationForm, LivestreamForm
from app.models import Configuration, User, Livestream

BASE_DIR = os.getcwd()

'''
@bp.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(stream_with_context(settings.generate()),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
'''

BASE_DIR = os.getcwd()

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
	if current_user.is_authenticated:
		title = current_user.full_name
	else:
		title = "Dotmole Cloud"
	return render_template('pages/placeholder.dashboard.html', title=title)

@bp.route('/launch', methods=['POST'])
@login_required
def launch():
	# Starting Livestream
	settings.init()  # initializing global variables
	# start a thread that will perform motion detection
	return redirect(url_for('main.dashboard_activity'))

@bp.route('/stop', methods=['POST'])
@login_required
def stop():
	settings.terminate()
	return redirect(url_for('main.dashboard_activity'))

@bp.route('/dashboard/activity')
@login_required
def dashboard_activity():
	timestamp = datetime.datetime.now()
	
	NUMBER_OF_LIVESTREAM = len(list(Livestream.query.filter_by(id_user=current_user.get_id())))
	LAST_SEEN = timestamp.strftime("%A")
	#VOLUME = os.path.getsize("data/motion/recorder.avi")/1000000
	data = {"number_of_livestreams": NUMBER_OF_LIVESTREAM,
			"last_seen": LAST_SEEN}
	return render_template('pages/placeholder.dashboard_activity.html', data=data)

# API to get images with name
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

@bp.route('/snitcher/add/people', methods=['POST'])
def add_people():
	print(request.files)
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')

	errors = {}
	success = False

	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
		
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 500
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 500
		return resp

@bp.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# Define
# configuration type - default / custom
# configuration_name - none    / <any_name>
@bp.route('/livestream', methods=['GET', 'POST'])
@login_required
def livestream():
	form = LivestreamForm() # Taking in the form
	default = {'services': 'motion', 'livestream_connected': 0}
	if form.is_submitted():
		if request.form["configuration_type"] == 'default': # type: default, name: any (doesn't matter)
			config = Configuration.query.filter_by(name=request.form["configuration_name"]).first()
			livestream = Livestream(user=current_user, config=config, name=form.name.data, internal_ip=form.internal_ip.data,configuration_name="default",configuration_type=form.configuration_type.data)
		else: # type custom, name: any (matters)
			try:
				config = Configuration.query.filter_by(name=request.form["configuration_name"])
				livestream = Livestream(user=current_user, config=config, internal_ip=request.form["internal_ip"],configuration_name=request.form["configuration_name"],configuration_type=request.form["configuration_type"])
			except expression as identifier:
				flash('Invalid configuration name', 'error')
				print("Invalid configuration name")
				livestreams = Livestream.query.filter_by(id_user=current_user.get_id()).all()
				return redirect(url_for('main.livestream', form=form, livestreams=livestreams))
		db.session.add(livestream)
		db.session.commit()
	livestreams = Livestream.query.filter_by(id_user=current_user.get_id()).all()
	form.configuration_name.choices = [(x.name, x.name) for x in Configuration.query.filter_by(id_user=current_user.get_id())]
	return render_template('pages/placeholder.livestream.html', form=form, livestreams=livestreams)

@bp.route('/livestream/view')
@login_required
def viewlivestream():
	return redirect(url_for('static', filename='motion/recorder.avi'))

@bp.route('/storage')
@login_required
def storage():
	footages = os.listdir('data/motion/')
	return render_template('pages/placeholder.videoshortner.html', footages=footages)

@bp.route('/snitcher/view/people')
@login_required
def viewpeople():
	PEOPLE = os.listdir('data/people')
	return render_template('pages/placeholder.viewpeople.html')

@bp.route('/snitcher/view/configurations', methods=['GET', 'POST'])
def viewconfig():
	form = ConfigurationForm()
	if form.is_submitted():
		configuration = Configuration(name=form.name.data, \
									description=form.description.data, \
									type='custom', services=form.services.data, \
									livestream_connected=0, \
									user=current_user)
		db.session.add(configuration)
		db.session.commit()
		return redirect(url_for("main.viewconfig"))
	configurations = Configuration.query.filter_by(id_user=current_user.get_id()).all()
	return render_template('pages/placeholder.viewconfig.html', configurations=configurations, form=form)

@bp.route('/snitcher/view/messages')
def viewnew():
    return render_template('pages/placeholder.viewmessages.html')

@bp.route('/contact')
@login_required
def contact():
    return render_template('pages/placeholder.contact.html')

@bp.route('/profile')
@login_required
def profile():
	
    return render_template('pages/placeholder.profile.html')

# Error handlers.
@bp.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404