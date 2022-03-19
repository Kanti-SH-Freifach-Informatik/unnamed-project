from unnamedproject import db

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    active_player = db.Column(db.Integer, nullable=True)
    top_card = db.Column(db.String(10), nullable=True)
    players = db.relationship("GamePlayer")