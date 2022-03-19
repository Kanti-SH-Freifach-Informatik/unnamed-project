from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('unnamedproject.config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from unnamedproject.models import Game, GamePlayer, Player
import unnamedproject.views