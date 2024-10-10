from typing import List, Optional
import pandas as pd
import streamlit as st 
from data import (
    get_top_k_games,
    get_total_plays,
    get_unique_games,
)
from plots import (
    show_wins_heatmap
)
from constants import (
    DATE_BINS,
    DATE_BIN_TABS
)

def play_stats_metric_cols(
        user_plays_df: pd.DataFrame,
        user_name: str,
        prev_days: Optional[int],
    ) -> None:
    '''Displays play stats metric columns'''
    total_cols = st.columns(4)
    top_5_cols = st.columns(5)

    top_5_games = get_top_k_games(
        user_plays_df,
        user_name,
        prev_days=prev_days,
    )
    total_plays = get_total_plays(user_plays_df, user_name, prev_days)
    unique_games = get_unique_games(user_plays_df, user_name, prev_days)
    with total_cols[1]:
        st.metric(
            label='Total Plays',
            value=total_plays
        )
    with total_cols[2]:
        st.metric(
            label='Unique Plays',
            value=unique_games
        )
    for (game, plays), top_5_col in zip(top_5_games, top_5_cols):
        with top_5_col:                                
            st.metric(
                label=game,
                value=plays,
            )

def play_stats_tab(user_plays_df: pd.DataFrame, user_name: str, games_selected: Optional[List[str]]) -> None:
    '''Displays play statistics tabs'''
    for date_bin, tab in zip(DATE_BINS, st.tabs(DATE_BIN_TABS)):
        with tab:
            if date_bin:
                st.markdown(f'## Plays Last {date_bin} Days')
            else:
                st.markdown(f'## Plays All Time')
            play_stats_metric_cols(user_plays_df, user_name, prev_days=date_bin)

def win_stats_tab(user_plays_df: pd.DataFrame, user_name: str, games_selected: Optional[List[str]]) -> None:
    '''Displays win statistics tabs'''
    for date_bin, tab in zip(DATE_BINS, st.tabs(DATE_BIN_TABS)):
        with tab:
            if date_bin:
                st.markdown(f'## Wins Last {date_bin} Days')
            else:
                st.markdown(f'## Wins All Time')
            show_wins_heatmap(user_plays_df, date_bin, games_selected)