from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
from hearbetweenthelines import app
import os


@app.route('/', methods =['GET','POST'])
def home():
	if request.method == "POST":
		file = request.files['musicfile']
		if file:
			#and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	return render_template('HomePage.html')
