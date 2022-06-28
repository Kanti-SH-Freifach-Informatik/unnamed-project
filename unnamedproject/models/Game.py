from enum import Enum
from unnamedproject import db
from unnamedproject.models.Card import Card, CardValue
from unnamedproject.utilities.card_utilities import is_playable


class GameState(Enum):
    NOT_STARTED = 0
    STARTED = 1
    FINISHED = 2


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    active_player = db.Column(db.Integer, nullable=False)
    top_card = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Enum(GameState), nullable=False,
                      default=GameState.NOT_STARTED)
    game_players = db.relationship(
        "GamePlayer", back_populates="game", order_by="GamePlayer.order")
    reverse = db.Column(db.Boolean, default=False, nullable=False)
    n_players = db.Column(db.Integer, nullable=False, default=4)

    def play_card(self, played_card):
        player = self.game_players[self.active_player]
        hand = player.get_hand()
        top_card = self.get_top_card()
        if len(hand) > played_card and is_playable(top_card, hand[played_card]):
            card = hand[played_card]
            self.top_card = str(card)
            hand.pop(played_card)
            player.set_hand(hand)
            if card.value == CardValue.REVERSE:
                self.reverse = not self.reverse

            if card.value == CardValue.SKIP:
                self.active_player = (
                    self.active_player + 2*self.get_multiplier()) % len(self.game_players)
            else:
                self.active_player = (
                    self.active_player + 1*self.get_multiplier()) % len(self.game_players)

    def draw_card(self):
        player = self.game_players[self.active_player]
        hand = player.get_hand()
        hand.append(Card())
        player.hand = player.set_hand(hand)
        self.active_player = (self.active_player + 1 *
                              self.get_multiplier()) % len(self.game_players)

    def handle_ai(self):
        player = self.game_players[self.active_player]
        while player.check_ai():
            possible_card = player.possible_card(self)
            if possible_card is not None:
                self.play_card(possible_card)
                winner = self.get_winner()
                if winner is not None:
                    return winner
                    break
                player = self.game_players[self.active_player]
            else:
                self.draw_card()
                player = self.game_players[self.active_player]

    def get_top_card(self):
        return Card(representation=self.top_card)

    def is_not_started(self):
        return self.state == GameState.NOT_STARTED

    def finish_game(self):
        self.state = GameState.FINISHED

    def get_winner(self):
        for gp in self.game_players:
            if gp.check_win():
                return gp
            else:
                return None

    def get_multiplier(self):
        return -1 if self.reverse else 1

    def get_game_player_by_token(self, token):
        for gp in self.game_players:
            if gp.player.token == token:
                return gp
        return None

    def get_active_game_player(self):
        return self.game_players[self.active_player]
