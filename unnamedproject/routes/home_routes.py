from flask import Blueprint
from unnamedproject.controllers.home_controller import index

home_bp = Blueprint('home', __name__)

home_bp.route('/', methods=['GET'])(index)