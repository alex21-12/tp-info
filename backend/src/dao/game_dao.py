from business_object.game import Game
from dao.db_connection import DBConnection
from utils.log_utils import get_logger
from utils.singleton import Singleton

logger = get_logger(__name__)


class GameDao(metaclass=Singleton):
    def __init__(self):
        self.db = DBConnection()

    def create(self, game: Game) -> bool:
        """
        Insère un nouveau jeu et met à jour son id_game.
        Note : Si la colonne 'timestamp' est gérée automatiquement par PostgreSQL
        (ex: DEFAULT CURRENT_TIMESTAMP), vous pouvez la retirer de la requête INSERT.
        """
        query = """
            INSERT INTO game (id_player1, id_player2, game_mode, id_winner, detail, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id_game;
        """

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Exécution avec les attributs correspondants aux colonnes de la table
                    cursor.execute(
                        query,
                        (
                            game.id_player1,
                            game.id_player2,
                            game.game_mode,
                            game.id_winner,
                            game.detail,
                            game.timestamp,
                        ),
                    )

                    # Récupération de l'ID généré via RETURNING id_game
                    returned_id = cursor.fetchone()[0]
                    game.id_game = returned_id

                    conn.commit()
                    return True

        except Exception as e:
            print(f"Erreur lors de la création du jeu : {e}")
            return False

    def find_by_id(self, id: int) -> Game | None:
        """
        Récupère un jeu par son ID et le convertit en objet Game.
        """
        query = """
            SELECT id_game, id_player1, id_player2, game_mode, id_winner, detail, timestamp 
            FROM game 
            WHERE id_game = %s;
        """

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (id,))
                    row = cursor.fetchone()

                    if row:
                        # L'ordre d'indexation correspond à l'ordre du SELECT
                        return Game(
                            id_game=row[0],
                            id_player1=row[1],
                            id_player2=row[2],
                            game_mode=row[3],
                            id_winner=row[4],  # Gère naturellement le [NULL] affiché dans DBeaver
                            detail=row[5],
                            timestamp=row[6],
                        )

                    return None

        except Exception as e:
            print(f"Erreur lors de la recherche du jeu avec l'ID {id} : {e}")
            return None

    def find_all_by_player(self, id_player: int) -> list[Game]:
        """
        Récupère toutes les parties impliquant un joueur spécifique
        (qu'il soit joueur 1 ou joueur 2) et renvoie une liste d'objets Game.
        """
        query = """
            SELECT id_game, id_player1, id_player2, game_mode, id_winner, detail, timestamp 
            FROM game 
            WHERE id_player1 = %s OR id_player2 = %s
            ORDER BY timestamp DESC;
        """

        games = []

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # On passe l'ID du joueur deux fois pour couvrir les deux conditions (id_player1 et id_player2)
                    cursor.execute(query, (id_player, id_player))

                    # fetchall() récupère tous les enregistrements correspondants
                    rows = cursor.fetchall()

                    for row in rows:
                        # On instancie un objet Game pour chaque ligne trouvée
                        game = Game(
                            id_game=row[0],
                            id_player1=row[1],
                            id_player2=row[2],
                            game_mode=row[3],
                            id_winner=row[4],
                            detail=row[5],
                            timestamp=row[6],
                        )
                        games.append(game)

            return games

        except Exception as e:
            print(f"Erreur lors de la recherche des parties pour le joueur {id_player} : {e}")
            return []  # Retourne une liste vide en cas d'erreur
