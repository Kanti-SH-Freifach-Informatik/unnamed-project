from datetime import datetime
from unnamedproject import db
from unnamedproject.models.Game import Game


class Message(db.Model):
    _tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.ForeignKey('games.id'))
    player_id = db.Column(db.ForeignKey('players.id'))
    message = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default = lambda: datetime.now())
    player = db.relationship("Player")
    game = db.relationship("Game", back_populates="messages", cascade="all, delete")

    
        