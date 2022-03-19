from unnamedproject import db

class GamePlayer(db.Model):
    _tablename__ = 'games_players'
    game_id = db.Column(db.ForeignKey('games.id'), primary_key=True)
    player_id = db.Column(db.ForeignKey('players.id'), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String(1000), nullable=False)
    player = db.relationship("Player", back_populates="games")
    game = db.relationship("Game", back_populates="game_players", cascade="all, delete")