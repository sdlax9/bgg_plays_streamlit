import streamlit as st
from data import (
    fetch_user_plays,
)
from tabs import(
    play_stats_tab,
)

st.set_page_config(layout="wide")

with st.sidebar:
    user_name = st.text_input(
        'BGG Username',
    )
    st.session_state['user_name'] = user_name

if user_name:
    try:
        user_plays_df = fetch_user_plays(user_name)
        st.session_state['user_plays_df'] = user_plays_df
    except Exception as e:
        print(e)


    st.markdown(f'# {user_name}')
    st.divider()

    play_stats = st.tabs([
        'Play Statistics'
    ])
    play_stats_tab(user_plays_df, user_name)