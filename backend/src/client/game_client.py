import requests

# N'oubliez pas d'importer votre classe Game au début du fichier
# from src.model.game import Game (ou le chemin correspondant à votre projet)


def get_games() -> list[Game]:
    """
    Appelle l'API externe pour récupérer la liste des parties (games)
    et les transforme en une liste d'objets métiers Game.
    """
    # 1. Appeler le point de terminaison (endpoint)
    # Remplacez "URL_DE_VOTRE_API" par l'URL réelle fournie dans votre TP
    url = "http://localhost:5555"
    r = requests.get(url)

    # 2. Vérifier la réponse
    # Cette méthode va automatiquement déclencher une erreur si l'API
    # renvoie un code d'erreur (comme 404 ou 500)
    r.raise_for_status()

    # 3. Récupérer le JSON (qui est une liste de dictionnaires)
    data = r.json()

    # 4. Convertir en une liste d'objets Game
    games_list = []

    # Itérer sur chaque élément de la liste un par un
    for element in data:
        # Création de l'objet Game en utilisant .get() pour sécuriser l'extraction
        game_object = Game(
            id=element.get("id"),
            players_list=element.get("players_list", []),  # Valeur par défaut: liste vide
            winner_name=element.get("winner_name"),
            location_name=element.get("location_name"),
            duration_seconds=element.get("duration_seconds"),
            mode_type=element.get("mode_type"),
        )

        # Ajouter l'objet à notre liste finale
        games_list.append(game_object)

    return games_list
