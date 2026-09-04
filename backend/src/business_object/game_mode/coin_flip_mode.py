import secrets
from datetime import datetime

from business_object.game import Game
from business_object.game_mode.game_mode import GameMode
from business_object.player import Player


class CoinFlipMode(GameMode):
    """Game mode: Heads or Tails."""

    def play(self, p1: Player, p2: Player, choice: str = "heads") -> Game:
        choice = choice.lower()
        if choice not in ["heads", "tails"]:
            raise ValueError(
                f"Invalid choice for CoinFlipMode: '{choice}'. Must be 'heads' or 'tails'."
            )
        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        return Game(
            player1=p1,
            player2=p2,
            game_mode="coinflip",
            winner=winner,
            description=f"{p1.username} choose {choice}. The coin landed on: {result}",
            timestamp=datetime.now(),
        )
