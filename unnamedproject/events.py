from unnamedproject import socketio, db
from flask import render_template
from flask_socketio import send, emit, join_room
from sqlalchemy.orm import joinedload

from unnamedproject.models.Game import Game, GameState
from unnamedproject.models.GamePlayer import GamePlayer
from unnamedproject.models.Player import Player
from unnamedproject.models.Message import Message
from unnamedproject.utilities.card_utilities import generate_hand


def get_game_and_current_player(game_id, token):
    game = Game.query.filter_by(id=game_id).options(
        joinedload(Game.game_players, GamePlayer.player)).first()
    current_player = Player.query.filter_by(token=token).first()
    return game, current_player


def get_template(game, player):
    if game.state == GameState.NOT_STARTED:
        return render_template('games/partials/waitingroom.html', game=game, current_player=player)
    if game.state == GameState.STARTED:
        return render_template('games/partials/gameroom.html', game=game, current_player=player)
    return render_template('games/partials/win.html', game=game, current_player=player)


@socketio.on('message')
def handle_message(message):
    send(message)


@socketio.on("join")
def on_join(data):
    token = data["token"]
    game_id = data["game_id"]
    room = f"{token}-{game_id}"
    join_room(room)
    game, current_player = get_game_and_current_player(game_id, token)
    for gp in game.game_players:
        if gp.player.token is not None and gp.player.token != '':
            emit("update", get_template(game, gp.player),
                 room=f"{gp.player.token}-{game.id}")


@socketio.on('start_game')
def on_start_game(data):
    game, current_player = get_game_and_current_player(
        data["game_id"], data["token"])
    curr_n_players = len(game.game_players)
    if(curr_n_players < game.n_players):
        for i in range(game.n_players - curr_n_players):
            p = Player(name=f"AI Spieler {i+1}", ai=True, token='')
            gp = GamePlayer(order=curr_n_players + i)
            gp.player = p
            gp.set_hand(generate_hand(7))
            game.game_players.append(gp)
    game.state = GameState.STARTED
    db.session.commit()
    for gp in game.game_players:
        if gp.player.token is not None and gp.player.token != '':
            emit("update", get_template(game, gp.player),
                 room=f"{gp.player.token}-{game.id}")


@socketio.on('play_card')
def on_play_card(data):
    game, current_player = get_game_and_current_player(
        data["game_id"], data["token"])
    played_card = data["played_card"]
    if current_player.id != game.get_active_game_player().player.id or played_card is None or not played_card.isdigit():
        return
    played_card = int(played_card)
    game.play_card(played_card)
    winner = game.get_winner()
    if winner is not None:
        game.finish_game()
    else:
        game.handle_ai()
        winner = game.get_winner()
        if winner is not None:
            game.finish_game()
    db.session.commit()
    for gp in game.game_players:
        if gp.player.token is not None and gp.player.token != '':
            emit("update", get_template(game, gp.player),
                 room=f"{gp.player.token}-{game.id}")


@socketio.on('draw_card')
def on_draw_card(data):
    game, current_player = get_game_and_current_player(
        data["game_id"], data["token"])
    if current_player.id != game.get_active_game_player().player.id:
        return
    game.draw_card()
    game.handle_ai()
    winner = game.get_winner()
    if winner is not None:
        game.finish_game()
    db.session.commit()
    for gp in game.game_players:
        if gp.player.token is not None and gp.player.token != '':
            emit("update", get_template(game, gp.player),
                 room=f"{gp.player.token}-{game.id}")

@socketio.on("chat")
def chat(data):
    game, current_player = get_game_and_current_player(
        data["game_id"], data["token"])
    message = data["message"]
    if message is None:
        return
    m = Message(message= message)
    m.player = current_player
    game.messages.append(m)
    db.session.commit()
    for gp in game.game_players:
        if gp.player.token is not None and gp.player.token != '':
            emit("update", get_template(game, gp.player),
                 room=f"{gp.player.token}-{game.id}")
