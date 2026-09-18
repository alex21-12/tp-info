from unittest.mock import patch

import pytest
from fastapi import HTTPException

from business_object.game import Game
from business_object.player import Player
from service.game_service import GameService


# 1. Fixture pour initialiser le service
@pytest.fixture
def game_service():
    return GameService()


# 2. Fixture des fausses données
@pytest.fixture
def mock_games():
    # On crée de faux objets Player pour les injecter dans les objets Game
    p1 = Player(id_player=1, username="p1", password="...", elo=1000)
    p2 = Player(id_player=2, username="p2", password="...", elo=1000)
    p3 = Player(id_player=3, username="p3", password="...", elo=1000)
    p4 = Player(id_player=4, username="p4", password="...", elo=1000)

    return [
        Game(
            id_game=1,
            player1=p1,
            player2=p2,
            game_mode="coinflip",
            id_winner=1,
            detail="...",
            timestamp="2026-09-18",
        ),
        Game(
            id_game=2,
            player1=p1,
            player2=p3,
            game_mode="dice",
            id_winner=3,
            detail="...",
            timestamp="2026-09-18",
        ),
        Game(
            id_game=3,
            player1=p4,
            player2=p1,
            game_mode="coinflip",
            id_winner=4,
            detail="...",
            timestamp="2026-09-18",
        ),
    ]


# 3. Test 1 : Sans filtre game_mode (retourne tout)
@patch("service.game_service.PlayerDao")
@patch("service.game_service.GameDao")
def test_find_all_games_no_mode(
    mock_game_dao_class, mock_player_dao_class, game_service, mock_games
):
    mock_player_dao = mock_player_dao_class.return_value
    mock_game_dao = mock_game_dao_class.return_value

    mock_player_dao.find_by_id.return_value = Player(
        id_player=1, username="test_player", password="...", elo=1000
    )
    mock_game_dao.find_all_by_player.return_value = mock_games

    result = game_service.find_all_by_player_and_game_mode(1, None)

    assert len(result) == 3
    mock_player_dao.find_by_id.assert_called_once_with(1)
    mock_game_dao.find_all_by_player.assert_called_once_with(1)


# 4. Test 2 : Avec filtre game_mode
@patch("service.game_service.PlayerDao")
@patch("service.game_service.GameDao")
def test_find_all_games_with_mode(
    mock_game_dao_class, mock_player_dao_class, game_service, mock_games
):
    mock_player_dao = mock_player_dao_class.return_value
    mock_game_dao = mock_game_dao_class.return_value

    mock_player_dao.find_by_id.return_value = Player(
        id_player=1, username="test_player", password="...", elo=1000
    )
    mock_game_dao.find_all_by_player.return_value = mock_games

    result = game_service.find_all_by_player_and_game_mode(1, "coinflip")

    assert len(result) == 2
    assert all(game.game_mode == "coinflip" for game in result)


# 5. Test 3 : Joueur inexistant (déclenche une erreur 404)
@patch("service.game_service.PlayerDao")
def test_find_all_games_player_not_found(mock_player_dao_class, game_service):
    mock_player_dao = mock_player_dao_class.return_value
    mock_player_dao.find_by_id.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        game_service.find_all_by_player_and_game_mode(999, "dice")

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Player not found"
