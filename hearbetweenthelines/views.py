from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
from hearbetweenthelines import app, ALLOWED_EXTENSIONS
from encrypt import extract, hide
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods =['GET','POST'])
def home():
    if request.method == "POST":
        text = request.form['message']
        if text != "":
			messageFile = open("Message.txt","w+")
			messageFile.write(text)
			messageFile.close()
			file = request.files['musicfile']
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				hide("Message.txt", filename, '1', "MixedTape.wav")
			else:
				print 'Add the right file you dumb fuck'
        else:
			file = request.files['encryptedfile']
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				text = extract(filename, '1')
				messageFile = open("DecodedMessage.txt","w+")
				messageFile.write(text)
				messageFile.close()
			else:
				print 'Add the right file you dumb fuck'

    return render_template('index.html')
