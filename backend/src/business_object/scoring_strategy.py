from business_object.game import Game

class ScoringStrategy():

    @classmethod
    def calculate_expected_score(cls, elo_a, elo_b) -> float:
        """Calculates the probability of player A winning against player B.
        Args:
            elo_a (float): The current Elo rating of first player.
            elo_b (float): The current Elo rating of second player.

        Returns:
            float: The expected score for player 1 (between 0 and 1).
        """
        return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    
    @classmethod
    def calculate_new_ratings(cls, elo_a, elo_b, player_a_won: bool) -> tuple[int, int]:
        """Computes the new Elo ratings for two players after a match.
        Args:
            elo_a (float): Current Elo of player 1.
            elo_b (float): Current Elo of player 2.
            player_a_won (bool): True if player 1 won, False if player 2 won.
        Returns:
            tuple[int, int]: A tuple containing (new_elo1, new_elo2).
        """
        k_factor = int(os.environ["ELO_K_FACTOR"])

        score_a = 1.0 if player_a_won else 0.0
        score_b = 1.0 - score_a

        new_elo_a = round(elo_a + k_factor * (score_a - cls.calculate_expected_score(elo_a, elo_b)))
        new_elo_b = round(elo_b + k_factor * (score_b - cls.calculate_expected_score(elo_b, elo_a)))

        return new_elo_a, new_elo_b

    @classmethod
    def update_player_ratings(cls, p1, p2, game: Game):
        """Calculates and updates the elo attributes of the players.
        No update if there is no winner (Draw).
        """
        # 1. Determine the actual score for Player 1 based on the winner
        if game.winner == game.player1:
            score_p1 = 1.0
        elif game.winner == game.player2:
            score_p1 = 0.0
        else:
            score_p1 = 0.5  # Draw

        # 2. Calculate new ratings
        new_elo_p1, new_elo_p2 = self.calculate_new_ratings(
            rating_a=game.player1.elo, 
            rating_b=game.player2.elo, 
            score_a=score_p1
        )

        # 3. Apply the new ratings to the player objects
        game.player1.elo = new_elo_p1
        game.player2.elo = new_elo_p2