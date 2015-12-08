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
    msg1 = ""
    msg2 = ""
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
                if filename.rsplit('.', 1)[1] == "wav":
                    os.system("./wavstego/wavstego -e 1234 -m Message.txt -a "+filename+" -o MixedTape.wav")
                else:
                    os.system("./mp3stego/mp3stego -b 320 -e Message.txt -p 1234 "+filename+" MixedTape.mp3")
                #hide("Message.txt", filename, '1', "MixedTape.mp3")
                msg1 = "Success!"
            else:
                msg1 = "Error: Please enter a proper music file"
        else:
            file = request.files['encryptedfile']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #text = extract(filename, '1')
                #messageFile = open("DecodedMessage.txt","w+")
                #messageFile.write(text)
                #messageFile.close()
                if filename.rsplit('.', 1)[1] == "wav":
                    os.system("./wavstego/wavstego -d 1234 -a MixedTape.wav")
                else:
                    os.system("./mp3stego/mp3stego -p 1234 MixedTape.mp3")
                msg2 = "Success!"
            else:
                msg2 = "Error: Please enter a proper music file"
    return render_template('index.html',message1 = msg1, message2 = msg2)
