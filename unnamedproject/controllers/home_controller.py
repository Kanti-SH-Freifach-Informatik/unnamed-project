from flask import render_template

# GET /
def index():
    return render_template('home.html')