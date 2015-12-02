from flask import Flask
from flask import render_template
import os
import getpass


user = getpass.getuser()
UPLOAD_FOLDER = "/tmp"
#UPLOAD_FOLDER = '/Users/rohansubramaniam/Documents/FreshmanYear/CS196/hearbetweenthelines'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print "this did happen"
    print os.getcwd()

import views
