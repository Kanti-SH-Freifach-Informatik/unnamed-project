from flask import render_template

# GET /
def index():
    name = "Eis"
    return render_template('waitinglobby.html', name=name)