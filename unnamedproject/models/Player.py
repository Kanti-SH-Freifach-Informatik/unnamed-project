import random
import string

from app import db

def generate_token():
    def get_random_string():
        return ''.join(random.choice(string.ascii_letters) for i in range(30))

    token = get_random_string()
    while Player.query.filter_by(token=token).limit(1).first() is not None:
        token = get_random_string()

    return token


class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(30), default=generate_token)
    games = db.relationship('GamePlayer', back_populates='player')
    ai= db.Column(db.Boolean, default=False, nullable = False)