from typing import Literal
import pandas as pd
import streamlit as st
import altair as alt

from data import (
    get_active_players
)

def show_wins_heatmap(
    user_plays_df: pd.DataFrame,
    date_bin: Literal['yearweek', 'yearmonthdate', ] # TODO these should correspond to the tab
)