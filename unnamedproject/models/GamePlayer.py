from unnamedproject import db
from unnamedproject.models.Card import Card
from unnamedproject.utilities.card_utilities import parse_hand_str, stringify_hand


class GamePlayer(db.Model):
    _tablename__ = 'games_players'
    game_id = db.Column(db.ForeignKey('games.id'), primary_key=True)
    player_id = db.Column(db.ForeignKey('players.id'), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    hand = db.Column(db.String(1000), nullable=False)
    player = db.relationship("Player", back_populates="games")
    game = db.relationship("Game", back_populates="game_players", cascade="all, delete")

    def get_hand(self):
        return parse_hand_str(self.hand)
    
    def set_hand(self, hand):
        def sort_key(c):
            return (c.color.value, c.value.value)
        hand = sorted(hand,key = sort_key)
        self.hand = stringify_hand(hand) 
        return self.hand

    def check_win(self):
        for i in self.hand:
            if i == "":
                return True

    def check_ai(self):
        return self.player.ai
        
    
    def possible_card(self, game):
        for i, c in enumerate(self.get_hand()):
            if c.color == game.get_top_card().color or c.value == game.get_top_card().value:
                return i
        return None