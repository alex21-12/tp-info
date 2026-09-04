from datetime import datetime

from business_object.player import Player


class Game:
    """
    Business object representing a completed game session.
    Stores information about the participants, the mode played,
    the outcome, and the timestamp.
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        game_mode: str,
        winner: Player | None,
        description: str,
        timestamp: datetime,
        id_game: int = None,
    ):
        self.id_game = id_game
        self.player1 = player1
        self.player2 = player2
        self.game_mode = game_mode
        self.winner = winner
        self.description = description
        self.timestamp = timestamp

    def __str__(self) -> str:
        """Returns a human-readable string including the game mode."""
        winner_name = self.winner.username if self.winner else "Draw"
        return f"{self.game_mode} between {self.player1.username} and {self.player2.username}\n  {self.description}\n  Winner: {winner_name}"
