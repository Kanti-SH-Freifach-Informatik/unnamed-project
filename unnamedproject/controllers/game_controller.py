from flask import render_template, request
from sqlalchemy.orm import joinedload

from unnamedproject import db
from unnamedproject.decorators.auth import current_player_required
from unnamedproject.models.Game import Game, GameState
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card
from unnamedproject.utilities.card_utilities import generate_hand


# GET /
def index():
    games = Game.query.all()
    return render_template('games/index.html', games=games)

# GET /:game_id
@current_player_required
def show(current_player, game_id):
    game = Game.query.filter_by(id=game_id).first()
    return render_template('games/show.html', current_player=current_player, game=game)

# POST /
@current_player_required
def create(current_player):
    n = request.form["number-of-players"]
    g = request.form["game-name"]
    if n  is not None and n.isdigit() and int(n)>=2 and int(n)<=8 and g is not None :
        top_card = Card()
        game = Game(active_player= 0, top_card=str(top_card), name=g, n_players=n)
        gp = GamePlayer(order=0)
        gp.player = current_player
        gp.set_hand(generate_hand(7))
        game.game_players.append(gp)
        db.session.add(game)
        db.session.commit()
        return render_template("games/show.html", current_player=current_player, game=game)
    else : 
        return render_template('home/create-game.html')

# GET /join/:game_id
@current_player_required
def join(current_player, game_id):
    game = Game.query.filter_by(id=game_id).first()
    if current_player.id not in map(lambda gp : gp.player.id, game.game_players):
        gp = GamePlayer(order=len(game.game_players))
        gp.player = current_player
        gp.set_hand(generate_hand(7))
        game.game_players.append(gp)
        db.session.commit()
    return render_template("games/show.html", current_player=current_player, game=game)

# DELETE /:game_id
def delete(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return "game deleted"


