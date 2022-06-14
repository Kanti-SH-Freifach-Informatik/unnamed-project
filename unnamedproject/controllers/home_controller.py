from flask import render_template

# GET /
def index():
    name = "Eis"
    return render_template('home/create-game.html', name=name)