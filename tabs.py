from typing import Optional
import pandas as pd
import streamlit as st 
from data import (
    get_top_k_games,
    get_total_plays,
    get_unique_games,
)
def play_stats_metric_cols(
        prev_days: Optional[int],
        user_plays_df: pd.DataFrame,
        user_name: str
    ) -> None:
    '''Displays play stats metric columns'''
    if prev_days:
        st.markdown(f'## Play Statistics Last {prev_days} Days')
    else:
        st.markdown('## Play Statistics All Time')
    col1, col2, col3, col4 = st.columns(4)

    top_5_games = get_top_k_games(
        user_plays_df,
        user_name,
        prev_days=prev_days,
    )
    total_plays = get_total_plays(user_plays_df, user_name, prev_days)
    unique_games = get_unique_games(user_plays_df, user_name, prev_days)
    with col2:
        for game, plays in top_5_games:
            st.metric(
                label=game,
                value=plays,
            )

    with col3:
        st.metric(
            label='Total Plays',
            value=total_plays
        )
        st.metric(
            label='Unique Games',
            value=unique_games
        )


def play_stats_tab(user_plays_df, user_name) -> None:
    '''Displays play statistics tabs'''
    tab_30_day, tab_year, tab_all = st.tabs(['Last 30 Days', 'Last 365 Days', 'All Time'])

    with tab_30_day:
        play_stats_metric_cols(30, user_plays_df, user_name)

    with tab_year:
        play_stats_metric_cols(365, user_plays_df, user_name)

    with tab_all:
        play_stats_metric_cols(None, user_plays_df, user_name)
