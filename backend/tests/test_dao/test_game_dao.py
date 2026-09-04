import os
from datetime import datetime
from unittest.mock import patch

import pytest

from business_object.game import Game
from business_object.player import Player
from dao.game_dao import GameDao
from utils.reset_database import ResetDatabase


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialize test data"""
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().run(test_dao=True)
        yield


def test_create_ok():
    """Successfully create a Game"""

    p1 = Player(username="a", elo=1000, email="test@test.io")
    p2 = Player(username="b", elo=1000, email="test@test.io")

    game = Game(
        player1=p1,
        player2=p2,
        game_mode="coinflip",
        winner=p1,
        description="test game",
        timestamp=datetime.now(),
    )

    # WHEN
    creation_ok = GameDao().create(game)

    # THEN
    assert creation_ok
    assert game.id_game


def test_find_by_id_existing():
    """Find a game by an existing id"""

    # GIVEN
    id_game = 8888

    # WHEN
    game = GameDao().find_by_id(id_game)

    # THEN
    assert isinstance(game, Game)
    assert game.id_game == id_game


def test_find_by_id_non_existing():
    """Find a game by a non-existing id"""

    # GIVEN
    id_game = 999999999

    # WHEN
    game = GameDao().find_by_id(id_game)

    # THEN
    assert game is None


def test_find_all_by_player_ok():
    """Find all games involving a specific player"""

    # GIVEN
    id_player = 998

    # WHEN
    games = GameDao().find_all_by_player(id_player)

    # THEN
    assert isinstance(games, list)
    for g in games:
        assert isinstance(g, Game)
        assert g.player1.id_player == id_player or g.player2.id_player == id_player
