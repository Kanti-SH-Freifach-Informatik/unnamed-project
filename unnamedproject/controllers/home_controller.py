from flask import render_template, request, make_response

from unnamedproject import db
from unnamedproject.models.Player import Player

# GET or POST /
def index():
    if request.method == 'POST':
        player_name = request.form['player-name']
        player = Player(name=player_name)
        db.session.add(player)
        db.session.commit()

        resp = make_response(render_template('home/create-game.html'))
        resp.set_cookie('token', player.token)
        return resp

    if 'token' in request.cookies:
        return render_template('home/create-game.html')
        
    return render_template('home/create-player.html')
