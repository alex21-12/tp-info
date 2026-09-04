from business_object.game_mode.game_mode import GameMode
from business_object.game_mode.coin_flip_mode import CoinFlipMode
from business_object.game_mode.dice_mode import DiceMode

class GameModeFactory:
    """Factory permettant de générer les instances de modes de jeu."""

    @classmethod
    def get_mode(cls, game_mode: str) -> GameMode:
        """
        Returns the corresponding GameMode object.
        
        Args:
            game_mode (str): The identifier of the game mode (e.g., 'coinflip', 'dice').
            
        Returns:
            GameMode: An instance of a class implementing GameMode.
            
        Raises:
            ValueError: If the requested game_mode is not supported.
        """
        mode = game_mode.lower()
        
        if mode == "coinflip":
            return CoinFlipMode()
        elif mode == "dice":
            return DiceMode()
        else:
            raise ValueError(f"Game mode not supported: {game_mode}")