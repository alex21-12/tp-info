import pytest


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
