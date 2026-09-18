from fastapi import HTTPException

from business_object.game_mode.game_mode_factory import GameModeFactory
from business_object.scoring_strategy import ScoringStrategy
from dao.game_dao import GameDao
from dao.player_dao import PlayerDao
from utils.log_utils import log


class GameService:
    """Service that manages games."""

    @log
    def play(self, id_player: int, id_opponent: int, game_mode: str, **kwargs):
        """Executes a single round of a game between two players.
        Args:
            id_player (int): The unique identifier of the first player.
            id_opponent (int): The unique identifier of the opponent.
            game_mode (str): The mode of the game being played.
        Returns:
            Game: The game object containing the match details.
        Raises:
            HTTPException: 400 if the two players are the same.
            HTTPException: 404 if one or both players are not found in the database.
        """
        if id_player == id_opponent:
            raise HTTPException(status_code=400, detail="Two different players required")

        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        mode = GameModeFactory.get_mode(game_mode)

        # 1. Jouer la partie
        game = mode.play(p1, p2, **kwargs)

        # 2. Mettre à jour les scores (Elo)
        ScoringStrategy.update_player_ratings(game)

        # 3. Mettre à jour les profils des joueurs en base de données
        PlayerDao().update(p1)
        PlayerDao().update(p2)

        # 4. Enregistrer l'historique de la partie en base de données
        GameDao().create(game)

        return game

    @log
    def find_by_id(self, id_game: int):
        """
        Récupère une partie spécifique grâce à son identifiant.

        Args:
            id_game (int): L'identifiant unique de la partie.

        Returns:
            Game: L'objet de la partie correspondante.

        Raises:
            HTTPException: 404 si la partie n'est pas trouvée dans la base de données.
        """
        game = GameDao().find_by_id(id_game)

        if not game:
            raise HTTPException(status_code=404, detail=f"Game with id {id_game} not found")

        return game

    @log
    def find_all_by_player_and_game_mode(self, id_player: int, game_mode: str = None):
        """
        Récupère l'historique des parties d'un joueur, avec un filtre optionnel sur le mode de jeu.

        Args:
            id_player (int): L'identifiant du joueur.
            game_mode (str, optional): Le mode de jeu à filtrer (ex: 'coinflip', 'dice').
                                       Si None, retourne toutes les parties.

        Returns:
            list[Game]: Une liste des parties correspondantes.

        Raises:
            HTTPException: 404 si le joueur n'existe pas.
        """
        # Vérification de l'existence du joueur via le DAO
        player = PlayerDao().find_by_id(id_player)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        # Récupération de tous les jeux du joueur via le DAO
        all_games = GameDao().find_all_by_player(id_player)

        # Si aucun mode n'est spécifié, on renvoie tout
        if game_mode is None:
            return all_games

        # Sinon, on filtre la liste en Python (list comprehension)
        filtered_games = [game for game in all_games if game.game_mode == game_mode]
        return filtered_games
