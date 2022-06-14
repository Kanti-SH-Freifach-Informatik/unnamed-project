from unnamedproject import db
from unnamedproject.models.Card import Card
from enum import Enum

class Status(Enum):
    NOT_STARTED = 0
    STARTED= 1
    FINISHED = 2

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    active_player = db.Column(db.Integer, nullable=False)
    top_card = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Enum(Status), nullable = False, default = Status.NOT_STARTED)
    game_players = db.relationship("GamePlayer", back_populates="game", order_by="GamePlayer.order")


    def get_top_card(self):
        return Card(representation=self.top_card)
