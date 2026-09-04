"""
Streamlit page for listing all players.

Retrieves and displays a list of registered players in a table, excluding sensitive data like passwords.

Endpoint used:
    GET /player
"""

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.title("Player list")
logger = get_page_logger("list_players")


check_authentification()

players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)

        df["url"] = df.apply(lambda row: f"/player_stats?id_player={row['id_player']}", axis=1)

        st.dataframe(
            df,
            column_config={
                "url": st.column_config.LinkColumn(label="Stats", display_text="📊"),
            },
            hide_index=True,
        )
    else:
        logger.info("No players found.")
        st.info("No players found.")


if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")
