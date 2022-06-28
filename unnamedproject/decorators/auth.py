from functools import wraps
from flask import request, render_template, make_response

from unnamedproject.models.Player import Player


def current_player_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'token' in request.cookies:
            current_player = Player.query.filter_by(
                token=request.cookies.get('token')).first()
            if current_player is not None:
                return f(current_player, *args, **kwargs)
        resp = make_response(render_template('home/create-player.html'))
        resp.delete_cookie('token')
        return resp
    return decorator
