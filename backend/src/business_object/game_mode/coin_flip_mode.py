import secrets
from datetime import datetime

from business_object.game_mode.game_mode import GameMode

from business_object.game import Game
from business_object.player import Player


class CoinFlipMode(GameMode):
    def play(self, p1: "Player", p2: "Player", **kwargs) -> Game:
        # On récupère le choix avec "heads" par défaut, comme dans votre code
        choice = kwargs.get("choice", "heads").lower()

        # Logique de votre ancien GameService
        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        return Game(
            player1=p1,
            player2=p2,
            game_mode="coinflip",
            description=result,  # On stocke le résultat (heads ou tails) ici
            timestamp=datetime.now(),
            winner=winner,
        )
