import os
import secrets

from fastapi import HTTPException

from dao.player_dao import PlayerDao
from utils.log_utils import log
from business_object.game_mode.game_mode import GameMode

class GameService:
    """Service that manages games."""

    @log
    def play(self, id_player: int, id_opponent: int, game_mode: str, **kwargs):
        """Executes a single round of a game between two players.
        Args:
            id_player (int): The unique identifier of the first player.
            id_opponent (int): The unique identifier of the opponent.
            game_mode (str): The mode of the game (e.g., 'coinflip', 'dice').
        Returns:
            Game: The resulting game object containing match details.
        Raises:
            HTTPException: 400 if the two players are the same.
            HTTPException: 404 if one or both players are not found in the database.
        """
        if id_player == id_opponent:
            raise HTTPException(status_code=400, detail="Two different players required")

        # 1. Get players (nothing to change)
        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        # 2. Get the game mode using the factory
        mode = GameModeFactory.get_mode(game_mode)

        # 3. Play the game
        # Les paramètres supplémentaires comme choice="heads" sont passés via **kwargs
        game = mode.play(p1, p2, **kwargs)

        # 4. Update elo of both players
        # En utilisant la méthode de classe que nous avons définie précédemment
        ScoringStrategy.update_player_ratings(game)

        # Sauvegarde en base de données (inchangé)
        PlayerDao().update(p1)
        PlayerDao().update(p2)

        # 5. Return a Game object
        return game

   