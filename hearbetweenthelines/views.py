from flask import render_template, request, redirect
from hearbetweenthelines import app

@app.route('/', methods =['GET','POST'])
def home():
	if request.method == "POST":
		mssg = request.form['message']
		f1 = request.form['musicfile']
		#f2 = request.form['encryptedfile']
		print mssg, f1 #f2 
	return render_template('HomePage.html')
