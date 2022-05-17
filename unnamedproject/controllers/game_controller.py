from flask import render_template, request

from unnamedproject import db
from unnamedproject.models.Game import Game
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Card import Card, CardValue
from unnamedproject.utilities.card_utilities import generate_hand_str, is_playable, stringify_hand

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
            gp = GamePlayer(order=i, hand=generate_hand_str(7))
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
    player = game.game_players[game.active_player]
    hand = player.get_hand()
    top_card = Card (representation = game.top_card)
    if len(hand) > played_card and is_playable (top_card,hand[played_card]):
        card = hand[played_card]
        game.top_card = str(card)
        hand.pop(played_card)
        player.set_hand(hand)
        if  player.check_win():
            active_player = game.active_player
            db.session.commit()
            return render_template("games/win.html", winner=active_player)
        else: 
            if card.value == CardValue.REVERSE :
                for gp in game.game_players:
                    gp.order = len(game.game_players) - gp.order - 1 
                game.active_player = len(game.game_players) - game.active_player - 1
                
            if  card.value == CardValue.SKIP :
                game.active_player = (game.active_player + 2 ) %len(game.game_players)
            else :
                game.active_player = (game.active_player + 1 ) %len(game.game_players)
            db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)

# POST /:game_id/draw
def draw(game_id):
    game = Game.query.filter_by(id=game_id).first()
    player = game.game_players[game.active_player]
    hand = player.get_hand()
    hand.append(Card())
    player.hand = player.set_hand(hand)
    game.active_player = (game.active_player + 1) %4
    db.session.commit()
    return render_template("gameroom/gameroom.html", game=game)

# DELETE /:game_id
def delete(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return "game deleted"