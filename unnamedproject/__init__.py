from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('unnamedproject.config')
socketio = SocketIO(app)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
    dbapi_con.execute('pragma foreign_keys=ON')

with app.app_context():
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)

# Assets
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/gameroom.scss', filters='pyscss', output='style.css')

assets.register('scss_all', scss)

if __name__ == "__main__":
    socketio.run(app)

from unnamedproject.models import Game, GamePlayer, Player
import unnamedproject.views
import unnamedproject.events
