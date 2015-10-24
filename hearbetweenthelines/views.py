from flask import render_template
from hearbetweenthelines import app

@app.route('/')
def home():
    return render_template('HomePage.html')