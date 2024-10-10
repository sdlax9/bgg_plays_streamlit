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