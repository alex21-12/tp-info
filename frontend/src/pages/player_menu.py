"""
Streamlit page for the main player menu.

Provides navigation to available actions such as listing players or playing games for logged-in users.
"""

import streamlit as st

from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.title("Main menu")
logger = get_page_logger("player_menu")

check_authentification()

player = st.session_state.get("player")

st.badge(f"Hello {player['username']}!", color="green")

st.write("Available actions:")

if st.button("List all players", use_container_width=True):
    st.switch_page("pages/list_players.py")

st.subheader("Games")

col1, col2 = st.columns(2)

with col1:
    if st.button("🪙 Play Coin Flip", use_container_width=True):
        st.switch_page("pages/play_coinflip.py")

with col2:
    if st.button("🎲 Play Dice Game", use_container_width=True):
        st.switch_page("pages/play_dice.py")

st.divider()

if st.button("Log out", type="primary", use_container_width=True):
    logger.info("Log out")
    del st.session_state["player"]
    st.switch_page("pages/home.py")
