import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.title("Player Stats")

logger = get_page_logger("player_stats")

query_params = st.query_params
player_id = query_params.get("id_player")
logger.info(f"Player {player_id} stats")

if player_id is not None:
    try:
        player_id = int(player_id)
        player_res = api_client.get(f"/player/{player_id}")

        if player_res["status_code"] == 200:
            player = player_res["data"]
            logger.info(f"Successfully retrieved profile for: {player['username']}")

            # --- PROFIL ---
            st.subheader(f"👤 {player['username']}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Elo Rating", player["elo"])
            with col2:
                st.write(f"**Email:** {player['email']}")
                st.write(f"**Pokemon Fan:** {'Yes' if player['pokemon_fan'] else 'No'}")
                st.checkbox("Pokemon Fan", value=player["pokemon_fan"], disabled=True)

            st.divider()

            # --- GAMES PLAYED ---
            st.subheader("Game History")

            logger.info(f"Fetching match history for player: {player['username']}")
            games_res = api_client.get(f"/game?id_player={player_id}")

            if games_res["status_code"] == 200:
                games_list = games_res["data"]
                logger.info(f"Found {len(games_list)} games for player {player_id}")

                if not games_list:
                    st.info("No games played yet.")
                else:
                    rows_for_df = []
                    for g in games_list:
                        opponent = (
                            g["player2"] if g["player1"]["id_player"] == player_id else g["player1"]
                        )
                        match g["winner"]:
                            case None:
                                result = "Draw"
                            case w if w["id_player"] == player_id:
                                result = "Win"
                            case _:
                                result = "Loss"
                        row = {
                            "Mode": g["game_mode"],
                            "Opponent": f"{opponent['username']} ({opponent['elo']})",
                            "Result": result,
                            "Date": g["timestamp"],
                        }
                        rows_for_df.append(row)

                    df = pd.DataFrame(rows_for_df)

                    st.dataframe(df, use_container_width=True, hide_index=True)

            else:
                logger.error(f"Failed to fetch games. Status: {games_res['status_code']}")
                st.error("Could not fetch games history.")

        else:
            logger.warning(f"Player not found. Status: {player_res['status_code']}")
            st.error(f"Player not found (Status: {player_res['status_code']})")

    except ValueError:
        logger.error(f"Invalid ID format: {player_id}")
        st.error("Invalid Player ID format in URL.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        st.error(f"An error occurred: {e}")
else:
    st.warning("No player selected. Please go back to the player list.")
