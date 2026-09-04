import secrets
from datetime import datetime

from business_object.game import Game
from business_object.game_mode.game_mode import GameMode
from business_object.player import Player


class DiceMode(GameMode):
    """Game mode: Rolling two dice."""

    def play(self, p1: Player, p2: Player) -> Game:
        d1 = secrets.choice(range(1, 7))
        d2 = secrets.choice(range(1, 7))

        winner = None
        description = f"Rolls: {p1.username} {d1} vs {d2} {p2.username}"

        if d1 > d2:
            winner = p1
        elif d2 > d1:
            winner = p2

        return Game(
            player1=p1,
            player2=p2,
            game_mode="dice",
            winner=winner,
            description=description,
            timestamp=datetime.now(),
        )
