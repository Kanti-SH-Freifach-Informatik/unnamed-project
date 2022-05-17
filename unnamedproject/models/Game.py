from unnamedproject import db
from unnamedproject.models.Card import Card

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    active_player = db.Column(db.Integer, nullable=False)
    top_card = db.Column(db.String(10), nullable=False)
    game_players = db.relationship("GamePlayer", back_populates="game", order_by="GamePlayer.order")

    def get_top_card(self):
        return Card(representation=self.top_card)
