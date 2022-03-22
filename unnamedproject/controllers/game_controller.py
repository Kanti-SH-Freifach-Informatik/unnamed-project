from flask import render_template

from unnamedproject import db
from unnamedproject.models.Game import Game
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card
from unnamedproject.utilities.card_utilities import generate_hand

# GET /
def index():
    return 'hello game'

# GET /:user_id
def show(game_id):
    return 'hello game number ' + str(game_id)

# POST /
def create():
    players = Player.query.limit(4).all()
    top_card = Card()
    game = Game(active_player= 0, top_card=str(top_card))
    for i, p in enumerate(players):
        # TODO füge hier Karten zur Hand des Spielers hinzu
        gp = GamePlayer(order=i, hand=generate_hand(7))
        gp.player = p
        game.game_players.append(gp)
    db.session.add(game)
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)

# POST /:user_id
def update(game_id):
    pass

# DELETE /:user_id
def delete(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return "game deleted"