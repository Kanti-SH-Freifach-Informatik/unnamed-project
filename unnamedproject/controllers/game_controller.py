from unnamedproject import db
from unnamedproject.models.Game import Game

# GET /
def index():
    return 'hello game'

# GET /:user_id
def show(game_id):
    return 'hello game number ' + str(game_id)

# POST /
def create():
    pass

# POST /:user_id
def update(game_id):
    pass

# DELETE /:user_id
def delete(game_id):
    pass