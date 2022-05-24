from flask import render_template, request

from unnamedproject import db
from unnamedproject.models.Game import Game
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card, CardValue
from unnamedproject.utilities.card_utilities import generate_hand, is_playable

# GET /
def index():
    return 'hello game'

# GET /:game_id
def show(game_id):
    return 'hello game number ' + str(game_id)

# POST /
def create():
    n = request.form["number-of-players"]
    if n is not None and n.isdigit() and int(n)>=2 and int(n)<=8 :
        players = Player.query.limit(int(n)).all()
        top_card = Card()
        game = Game(active_player= 0, top_card=str(top_card))
        for i, p in enumerate(players):
            gp = GamePlayer(order=i)
            gp.set_hand(generate_hand(7))
            gp.player = p
            game.game_players.append(gp)
        db.session.add(game)
        db.session.commit()
        return render_template("gameroom/gameroom.html", game=game)
    else : 
        return render_template('waitinglobby.html')



# POST /:game_id/:played_card
def update(game_id, played_card):
    game = Game.query.filter_by(id=game_id).first()
    game.play_card(played_card)
    db.session.commit()
    for gp in game.game_players:
        if gp.check_win():
            return render_template("games/win.html", game=game)
    else:
        return render_template("gameroom/gameroom.html", game=game)

# POST /:game_id/draw
def draw(game_id):
    game = Game.query.filter_by(id=game_id).first()
    game.draw_card()
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)

# DELETE /:game_id
def delete(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return "game deleted"