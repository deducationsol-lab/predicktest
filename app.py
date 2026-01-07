import streamlit as st
import requests
from datetime import datetime
import uuid
import pandas as pd
import plotly.express as px
import hashlib

# Page config
st.set_page_config(page_title="Meme-DICKTOR", page_icon="🤡", layout="wide")

# Super meme theme
st.markdown("""
<style>
    .stApp { background: linear-gradient(#000, #110033); color: #ff00ff; }
    .big-title {
        font-size: 6rem !important;
        text-align: center;
        background: linear-gradient(90deg, #ff00ff, #00ff00, #ffff00, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rave 2s infinite;
    }
    @keyframes rave { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
    .subtitle { font-size: 2rem; text-align: center; color: #00ff00; }
    .stButton > button {
        background: #ff00ff; color: black; font-weight: bold; border-radius: 50px; padding: 20px;
        box-shadow: 0 0 30px #ff00ff;
    }
    .market-card {
        background: #111; border: 5px dashed #00ff00; border-radius: 30px; padding: 40px; margin: 40px 0;
        box-shadow: 0 0 50px #ff00ff;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="big-title">Meme-DICKTOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">The Ultimate Prediction Market for X Memes & Viral Trends 🤡🗳️</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:2rem'>Bet on what goes viral next. Powered by degen energy!</p>", unsafe_allow_html=True)

# Wallet & Disclaimer (same as before)

# Meme Markets – Funny X Trend Examples
markets = [
    {"question": "Which animal meme wins January 2026?", "options": ["Cats 😹", "Dogs 🐶", "Frogs 🐸", "Birds 🐦", "Others 🦝"], "votes": {"Cats 😹": 0, "Dogs 🐶": 0, "Frogs 🐸": 0, "Birds 🐦": 0, "Others 🦝": 0}},
    {"question": "Will 'Skibidi Toilet' still be trending in Feb?", "options": ["Yes 🚽", "No 🪦", "Brainrot forever 🧠"], "votes": {"Yes 🚽": 0, "No 🪦": 0, "Brainrot forever 🧠": 0}},
    {"question": "Next big X trend format?", "options": ["AI Slop 🤖", "Cat Videos 😻", "Ratio Wars ⚔️", "Wholesome Memes 🥹"], "votes": {"AI Slop 🤖": 0, "Cat Videos 😻": 0, "Ratio Wars ⚔️": 0, "Wholesome Memes 🥹": 0}},
    {"question": "Most viral meme sound 2026?", "options": ["Ohio Rizz 🎶", "Skibidi Dop 🎵", "New Brainrot 🔄", "Classic Vine 🧓"], "votes": {"Ohio Rizz 🎶": 0, "Skibidi Dop 🎵": 0, "New Brainrot 🔄": 0, "Classic Vine 🧓": 0}},
    {"question": "Will 'Hawk Tuah' girl return in 2026?", "options": ["Yes spit on that thang 👅", "No she's gone 😢", "New version drops 🔥"], "votes": {"Yes spit on that thang 👅": 0, "No she's gone 😢": 0, "New version drops 🔥": 0}},
]

# Display funny markets
for market in markets:
    with st.container():
        st.markdown("<div class='market-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center'>{market['question']}</h2>", unsafe_allow_html=True)

        total = sum(market['votes'].values())
        cols = st.columns(len(market['options']))
        for idx, opt in enumerate(market['options']):
            with cols[idx]:
                perc = (market['votes'][opt] / total * 100) if total > 0 else 0
                st.markdown(f"<h3 style='text-align:center'>{opt}<br>{perc:.1f}%</h3>", unsafe_allow_html=True)
                if st.button(f"BET ON {opt}", key=f"bet_{market['question']}_{opt}", use_container_width=True):
                    market['votes'][opt] += 1
                    st.success(f"You bet on {opt}! De gen move 😈")
                    st.balloons()

        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center;padding:50px'>
    <h2>Meme-DICKTOR – Where X Trends Become Money 🤡💰</h2>
    <p>No financial advice. Just pure degen fun.</p>
</div>
""", unsafe_allow_html=True)
