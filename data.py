import datetime
from typing import Tuple, List, Optional
import pandas as pd
import streamlit as st
import libbgg
from libbgg.apiv2 import BGG

def extract_page_data(page_data: libbgg.infodict.InfoDict) -> Tuple[list, list]:
    """Extracts play and player data from a page"""
    plays = page_data['plays']['play']
    play_data = []
    players_data = []

    for play in plays:
        play_id = play['id']
        game = play['item']['name']
        date = play['date']
        plrs = play['players']['player']

        if isinstance(plrs, list): # multiple players
            plrs = [dict(plr) for plr in plrs]
            for plr in plrs:
                plr.update({'play_id': play_id})
                players_data.append(plr)
        else: # single player
            plrs = dict(plrs)
            plrs.update({'play_id': play_id})
            players_data.append(plrs)
        play_data.append(
            {
                'play_id': play_id,
                'game': game,
                'date': date,
            }
        )
    return play_data, players_data

def get_user_name_plays_df(
        user_plays_df: pd.DataFrame,
        user_name: str,
        prev_days: Optional[int] = None
    ) -> pd.DataFrame:
    '''Returns '''
    if prev_days:
        prev_date = datetime.datetime.today() - datetime.timedelta(days=prev_days)
        user_name_plays_df = user_plays_df[
            (user_plays_df['username'] == user_name) &
            (user_plays_df['date'] >= prev_date)]
    else:
        user_name_plays_df = user_plays_df[user_plays_df['username'] == user_name]
    return user_name_plays_df

@st.cache_data
def fetch_user_plays(username: str) -> pd.DataFrame:
    """Returns user plays DataFrame"""
    conn = BGG()
    plays_data = []
    players_data = []
    page = 1
    page_data = conn.get_plays(username=username, page=page)
    while 'play' in page_data['plays']:
        page_plays_data, page_players_data = extract_page_data(page_data)
        plays_data.extend(page_plays_data)
        players_data.extend(page_players_data)
        page += 1
        page_data = conn.get_plays(username=username, page=page)

    plays_df = pd.DataFrame(plays_data)
    players_df = pd.DataFrame(players_data)

    players_filt_df = players_df.set_index('play_id')
    plays_filt_df = plays_df.set_index('play_id')

    user_plays_df = players_filt_df.merge(
        plays_filt_df,
        how='left',
        left_index=True,
        right_index=True
    )
    user_plays_df['date'] = pd.to_datetime(user_plays_df['date'], format='%Y-%m-%d')
    return user_plays_df

@st.cache_data
def get_top_k_games(
    user_plays_df: pd.DataFrame,
    user_name: str,
    top_k: int = 5,
    prev_days: int = None,
) -> List[Tuple[str, int]]:
    '''Returns list of top k played games for user'''
    user_name_plays_df = get_user_name_plays_df(
        user_plays_df,
        user_name,
        prev_days,
    )
    user_plays_agg = user_name_plays_df.groupby('game')['game'].count()
    top_k_list = list(user_plays_agg.sort_values(ascending=False)[:top_k].items())
    return top_k_list
    
@st.cache_data
def get_total_plays(
    user_plays_df: pd.DataFrame,
    user_name: str,
    prev_days: int = None,
):
    '''Returns the total number of plays'''
    user_name_plays_df = get_user_name_plays_df(
        user_plays_df,
        user_name,
        prev_days,
    )
    return len(user_name_plays_df.index.unique())
    

@st.cache_data
def get_unique_games(
    user_plays_df: pd.DataFrame,
    user_name: str,
    prev_days: int = None,
) -> int:
    '''Returns number of unique games played'''
    user_name_plays_df = get_user_name_plays_df(
        user_plays_df,
        user_name,
        prev_days,
    )
    return len(user_name_plays_df['game'].unique())