import datetime
from typing import List, Literal, Optional
import pandas as pd
import streamlit as st
import altair as alt

from data import (
    get_active_players
)

def show_wins_heatmap(
    user_plays_df: pd.DataFrame,
    date_bin: Literal[30, 365, None],
    games_selected: Optional[List[str]]
):
    '''Displays heatmap of active player wins over time'''
    d3_date_formats = {
        30: 'monthdate',
        365: 'yearmonthdate',
        None: 'yearquarter'
    }
    active_players = get_active_players(user_plays_df=user_plays_df)

    wins_df = user_plays_df[user_plays_df['name'].isin(active_players)]
    if date_bin:
        wins_df = wins_df[wins_df['date'] >= (datetime.datetime.now() - datetime.timedelta(days=date_bin))]

    if games_selected:
        wins_df = wins_df[wins_df['game'].isin(games_selected)]
    
    heatmap = alt.Chart(wins_df).mark_rect().encode(
        alt.X(f"{d3_date_formats[date_bin]}(date):O", title="Date").axis(labelAngle=0),
        alt.Y("name:O").title("Month"),
        alt.Color("sum(win):Q").title(None),
        tooltip=[
            alt.Tooltip("sum(win):Q", title="Wins"),
        ]
    )
    st.altair_chart(heatmap, use_container_width=True)