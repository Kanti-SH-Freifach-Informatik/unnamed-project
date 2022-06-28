from flask import render_template, request
from sqlalchemy.orm import joinedload

from unnamedproject import db
from unnamedproject.decorators.auth import current_player_required
from unnamedproject.models.Game import Game, Status
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card
from unnamedproject.utilities.card_utilities import generate_hand


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
    curr_players = len(game.game_players)
    if(curr_players < game.n_players):
        for i in range(game.n_players - curr_players):
            p = Player(name=f"AI Spieler {i+1}", ai=True, token='')
            gp = GamePlayer(order=curr_players + i)
            gp.player = p
            gp.set_hand(generate_hand(7))
            game.game_players.append(gp)
    game.state = Status.STARTED
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)


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
        return render_template("games/waitingroom.html", game=game)
    else : 
        return render_template('home/create-game.html')

# GET /join/:game_id
@current_player_required
def join(current_player, game_id):
    game = Game.query.filter_by(id=game_id).first()
    if current_player.id in map(lambda gp : gp.player.id, game.game_players):
        return render_template("games/waitingroom.html", game=game)
    gp = GamePlayer(order=len(game.game_players))
    gp.player = current_player
    gp.set_hand(generate_hand(7))
    game.game_players.append(gp)
    db.session.commit()
    return render_template("games/waitingroom.html", game=game)



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


