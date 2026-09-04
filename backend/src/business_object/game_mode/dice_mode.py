import random
from datetime import datetime

from business_object.game.game_mode import Game

from business_object.game_mode.game_mode import GameMode


class DiceMode(GameMode):
    def play(self, p1: "Player", p2: "Player", **kwargs) -> Game:
        # Lancer des dés (de 1 à 6)
        roll_p1 = random.randint(1, 6)
        roll_p2 = random.randint(1, 6)

        # Détermination du vainqueur
        if roll_p1 > roll_p2:
            winner = p1
            desc = f"{p1.username} a gagné avec un {roll_p1} contre {roll_p2}."
        elif roll_p2 > roll_p1:
            winner = p2
            desc = f"{p2.username} a gagné avec un {roll_p2} contre {roll_p1}."
        else:
            winner = None
            desc = f"Match nul, les deux joueurs ont fait un {roll_p1}."

        return Game(
            player1=p1,
            player2=p2,
            game_mode="dice",
            description=desc,
            timestamp=datetime.now(),
            winner=winner,
        )
