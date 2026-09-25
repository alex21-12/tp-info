"""
Streamlit page for displaying player statistics.

Reads player ID from query parameters, fetches details from the API,
and displays key attributes (username, Elo rating, email, preferences).

Endpoints used:
    GET /player/{id_player}
"""

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.title("Player Statistics")
logger = get_page_logger("player_stats")

check_authentification()

# Get player ID from URL query parameters (e.g. ?id_player=4)
id_player = st.query_params.get("id_player")

if not id_player:
    st.error("No player ID provided in query parameters.")
    st.info("Expected URL format: `?id_player=<id>`")
    st.stop()

logger.info(f"Fetching stats for player ID: {id_player}")

# Call the API to fetch player attributes
response = api_client.get(f"/player/{id_player}")

if response.get("status_code") != 200:
    st.error(f"Error loading player: {response.get('data', 'Player not found')}")
    st.stop()

player_data = response["data"]

# Display Player Information
st.subheader(f"Player: {player_data.get('username')}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Elo Rating",
        value=player_data.get("elo", "N/A"),
    )

with col2:
    st.write(f"**Email:** {player_data.get('email', 'N/A')}")
    st.checkbox(
        label="Pokémon fan",
        value=bool(player_data.get("is_pokemon_fan", False)),
        disabled=True,
    )

if st.button("Back to menu"):
    st.switch_page("pages/player_menu.py")