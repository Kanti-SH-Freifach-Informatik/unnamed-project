from flask import Blueprint
from unnamedproject.controllers.game_controller import index, show, create, delete, join

game_bp = Blueprint('games', __name__)

game_bp.route('/', methods=['GET'])(index)
game_bp.route('/<int:game_id>', methods=['GET'])(show)
game_bp.route('/', methods=['POST'])(create)
game_bp.route('/join/<int:game_id>', methods=['GET'])(join)
game_bp.route('/<int:game_id>', methods=['DELETE'])(delete)
