from unittest.mock import MagicMock

from business_object.game import Game
from business_object.player import Player
from dao.game_dao import GameDao
from service.game_service import GameService

players = [
    Player(id_player=0, username="jp", elo=None, email=None, password=None),
    Player(id_player=1, username="lea", elo=None, email=None, password=None),
    Player(id_player=2, username="gg", elo=None, email=None, password=None),
]

games = [
    Game(players[0], players[1], "coinflip", players[0], None, None),
    Game(players[0], players[1], "coinflip", players[0], None, None),
    Game(players[1], players[2], "coinflip", players[1], None, None),
    Game(players[0], players[1], "dice", players[0], None, None),
]


def test_find_all_by_player_no_game_mode():

    # GIVEN
    GameDao().find_all_by_player = MagicMock(return_value=games)

    # WHEN
    res = GameService().find_all_by_player(id_player=1)

    # THEN
    assert len(res) == 4


def test_find_all_by_player_with_game_mode():

    # GIVEN
    GameDao().find_all_by_player = MagicMock(return_value=games)
    mode = "coinflip"

    # WHEN
    res = GameService().find_all_by_player(id_player=1, game_mode=mode)

    # THEN
    assert len(res) == 3
    for g in res:
        assert g.game_mode == mode
