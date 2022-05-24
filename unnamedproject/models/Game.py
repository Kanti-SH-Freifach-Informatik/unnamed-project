from unnamedproject import db
from unnamedproject.models.Card import Card, CardValue
from unnamedproject.utilities.card_utilities import is_playable


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    active_player = db.Column(db.Integer, nullable=False)
    top_card = db.Column(db.String(10), nullable=False)
    game_players = db.relationship("GamePlayer", back_populates="game",order_by="GamePlayer.order")

    def play_card(self, played_card):
        player = self.game_players[self.active_player]
        hand = player.get_hand()
        top_card = self.get_top_card()
        if len(hand) > played_card and is_playable (top_card, hand[played_card]):
            card = hand[played_card]
            self.top_card = str(card)
            hand.pop(played_card)
            player.set_hand(hand)
            if card.value == CardValue.REVERSE :
                for gp in self.game_players:
                    gp.order = len(self.game_players) - gp.order - 1 
                self.active_player = len(self.game_players) - self.active_player - 1
            
            if  card.value == CardValue.SKIP :
                self.active_player = (self.active_player + 2 ) %len(self.game_players)
            else :
                self.active_player = (self.active_player + 1 ) %len(self.game_players)
        while player.check_ai():
            if player.possible_card(self):
                card = player.ai_play_card(self)
                self.play_card(card)
            else:
                self.draw_card()

    def draw_card(self):
        player = self.game_players[self.active_player]
        hand = player.get_hand()
        hand.append(Card())
        player.hand = player.set_hand(hand)
        self.active_player = (self.active_player + 1) %4

    def get_top_card(self):
        return Card(representation=self.top_card)

