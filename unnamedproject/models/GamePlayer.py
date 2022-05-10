from unnamedproject import db
from unnamedproject.models.Card import Card
from unnamedproject.utilities.card_utilities import parse_hand_str, stringify_hand


class GamePlayer(db.Model):
    _tablename__ = 'games_players'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.ForeignKey('games.id'))
    player_id = db.Column(db.ForeignKey('players.id'))
    order = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String(1000), nullable=False)
    player = db.relationship("Player", back_populates="games")
    game = db.relationship("Game", back_populates="game_players", cascade="all, delete")

    def get_hand(self):
        return parse_hand_str(self.hand)
    
    def set_hand(self, hand):
        return stringify_hand(hand)    

    def check_win(self):
        return len(self.hand) == 0