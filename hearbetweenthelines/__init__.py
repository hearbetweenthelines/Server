from flask import Flask
from flask import render_template



UPLOAD_FOLDER = '/Users/rohansubramaniam/Documents/FreshmanYear/CS196/hearbetweenthelines'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import views
