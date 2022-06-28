from flask import render_template, request
from sqlalchemy.orm import joinedload

from unnamedproject import db
from unnamedproject.models.Game import Game, Status
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card, CardValue
from unnamedproject.utilities.card_utilities import generate_hand, is_playable


# GET /
def index():
    games = Game.query.all()
    return render_template('games/index.html', games=games)

# GET /:game_id
def show(game_id):
    game = Game.query.filter_by(id=game_id).first()
    return render_template('games/waitingroom.html', game=game)

# GET /:game_id
def start(game_id):
    game = Game.query.filter_by(id=game_id).first()
    game.state = Status.STARTED
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)


# POST /
def create():
    n = request.form["number-of-players"]
    g = request.form["game-name"]
    if n  is not None and n.isdigit() and int(n)>=2 and int(n)<=8 and g is not None :
        players = Player.query.limit(int(n)).all()
        top_card = Card()
        game = Game(active_player= 0, top_card=str(top_card),name=g)
        for i, p in enumerate(players):
            gp = GamePlayer(order=i)
            gp.set_hand(generate_hand(7))
            gp.player = p
            game.game_players.append(gp)
        db.session.add(game)
        db.session.commit()
        return render_template("games/waitingroom.html", game=game)
    else : 
        return render_template('home/create-game.html')


# POST /:game_id/:played_card
def update(game_id, played_card):
    game = Game.query.filter_by(id=game_id).options(joinedload(Game.game_players, GamePlayer.player)).first()
    game.play_card(played_card)
    winner = game.get_winner()
    if winner is not None:
        game.finish_game()
        db.session.commit()
        return render_template("games/win.html", game=game, winner=winner)
    else:    
        game.handle_ai()
        winner = game.get_winner()
        if winner is not None:
            game.finish_game()
            db.session.commit()
            return render_template("games/win.html", game=game, winner=winner)
        else:
            db.session.commit()
            return render_template("gameroom/gameroom.html", game=game)

# POST /:game_id/draw
def draw(game_id):
    game = Game.query.filter_by(id=game_id).first()
    game.draw_card()
    game.handle_ai()
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)

# DELETE /:game_id
def delete(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return "game deleted"


