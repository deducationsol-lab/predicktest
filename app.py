import streamlit as st
import requests
from datetime import datetime
import uuid
import pandas as pd
import plotly.express as px
import hashlib

# Page config
st.set_page_config(page_title="Pre-DICKTOR Beta", page_icon="🍆", layout="wide")

# High-tech neon dark theme
st.markdown("""
<style>
    .stApp { background: #000000; color: #e0ffe0; }
    .big-title {
        font-size: 5.5rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #39ff14, #ff00ff, #00ffff, #39ff14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neon-pulse 3s ease-in-out infinite alternate;
        text-shadow: 0 0 20px #39ff14;
    }
    @keyframes neon-pulse {
        from { text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14; }
        to { text-shadow: 0 0 20px #ff00ff, 0 0 40px #ff00ff; }
    }
    .subtitle { font-size: 2.2rem; text-align: center; color: #ff00ff; text-shadow: 0 0 15px #ff00ff; }
    .stButton > button {
        background: linear-gradient(45deg, #001a00, #1a0033);
        color: #39ff14;
        border: 2px solid #39ff14;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.3rem;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(57, 255, 20, 0.6);
    }
    .stButton > button:hover {
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.8);
        transform: translateY(-3px);
    }
    .market-card {
        background: rgba(10, 10, 30, 0.8);
        border: 3px solid #ff00ff;
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
    }
    .share-btn {
        background: linear-gradient(45deg, #ff00ff, #8000ff);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 0 25px #ff00ff;
    }
    .beta-badge {
        background: #ff00ff;
        color: black;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 0 20px #ff00ff;
        display: inline-block;
        margin: 10px 0;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# === SECURE ADMIN PASSWORD ===
EXPECTED_HASH = "6645adc23275824958437afdcc809d3027c4f772ee65ebd26846e943e6209437"

def check_admin_password(pwd: str) -> bool:
    return hashlib.sha256(pwd.encode()).hexdigest() == EXPECTED_HASH

# BETA TESTING MODE
st.markdown("<div class='beta-badge'>BETA TESTING MODE – SIMULATOR ACTIVE</div>", unsafe_allow_html=True)

# Disclaimer
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style='background:rgba(20,0,40,0.8);padding:50px;border-radius:20px;border:4px dashed #39ff14;text-align:center;box-shadow:0 0 40px rgba(57,255,20,0.4);max-width:800px;margin:auto'>
        <h1 style='color:#ff00ff'>🔴 BETA ACCESS</h1>
        <h2 style='color:#39ff14'>PRE-DICKTOR BETA SIMULATOR</h2>
        <p style='font-size:1.6rem;color:#b0ffb0'>
            This is a BETA test with simulated $DEDU.<br>
            No real money involved. For testing only.<br>
            Have fun and break things! 😏
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("EXIT BETA", type="secondary", use_container_width=True):
            st.stop()
    with col2:
        if st.button("ENTER BETA SIMULATOR", type="primary", use_container_width=True):
            st.session_state.disclaimer_accepted = True
            st.balloons()
            st.rerun()
    st.stop()

# Title
st.markdown('<h1 class="big-title">Pre-DICKTOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Beta Voting Simulator | 1,000,000 Simulated $DEDU per user 🗳️🍆</p>', unsafe_allow_html=True)

# User Registration for Beta Testing
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
    st.session_state.sim_dedu_balance = 0
    st.session_state.votes_cast = 0

if st.session_state.user_id is None:
    st.markdown("<h3 style='color:#39ff14;text-align:center'>REGISTER FOR BETA TESTING</h3>", unsafe_allow_html=True)
    username = st.text_input("Choose a Degen Name")
    if st.button("JOIN BETA – GET 1,000,000 SIMULATED $DEDU"):
        if username:
            st.session_state.user_id = str(uuid.uuid4())[:8]
            st.session_state.username = username
            st.session_state.sim_dedu_balance = 1000000  # 1 million simulated $DEDU
            st.session_state.votes_cast = 0
            st.success(f"Welcome {username}! You received 1,000,000 simulated $DEDU")
            st.balloons()
            st.rerun()
        else:
            st.warning("Enter a name!")

# Show user info
if st.session_state.user_id:
    st.sidebar.markdown(f"**Degen:** {st.session_state.username}")
    st.sidebar.markdown(f"**Sim $DEDU Balance:** {st.session_state.sim_dedu_balance:,.0f}")
    st.sidebar.markdown(f"**Votes Cast:** {st.session_state.votes_cast}")

# Live $DEDU Price for reference (real)
DEDU_MINT = "AqDGzh4jRZipMrkBuekDXDB1Py2huA8G5xCvrSgmpump"
try:
    response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{DEDU_MINT}").json()
    if response.get('pairs'):
        price = float(response['pairs'][0]['priceUsd'])
        st.sidebar.markdown(f"**Real $DEDU Price:** ${price:.10f}")
        cost_per_vote = 0.10 / price  # 10 cents in $DEDU
        st.sidebar.markdown(f"**Cost per Vote (real equiv):** ~{cost_per_vote:.0f} $DEDU")
    else:
        st.sidebar.markdown("**Real $DEDU Price:** Loading...")
except:
    st.sidebar.markdown("**Real $DEDU Price:** Offline")

# 10 Free Test Plays
if st.session_state.votes_cast < 10:
    remaining = 10 - st.session_state.votes_cast
    st.info(f"🎁 You have {remaining} FREE test votes remaining!")

# Markets
if 'markets' not in st.session_state:
    st.session_state.markets = []

# Leaderboard (real from users)
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# Update leaderboard
def update_leaderboard():
    if st.session_state.user_id:
        # Remove old entry for this user
        st.session_state.leaderboard = [entry for entry in st.session_state.leaderboard if entry['user_id'] != st.session_state.user_id]
        # Add updated
        st.session_state.leaderboard.append({
            "user_id": st.session_state.user_id,
            "username": st.session_state.username,
            "votes": st.session_state.votes_cast
        })
        # Sort and keep top 10
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x['votes'], reverse=True)[:10]

# Admin
with st.sidebar:
    st.markdown("### 🔐 ADMIN")
    pwd = st.text_input("Password", type="password")
    if check_admin_password(pwd):
        st.success("Access Granted")
        with st.form("create_market"):
            question = st.text_input("Question", "Which meme will dominate 2026?")
            options_input = st.text_area("Answers (one per line)", "BONK 🐶\nWIF 🧢\nPEPE 🐸\nPOPCAT 😼")
            date = st.date_input("Voting Ends")
            submitted = st.form_submit_button("LAUNCH")
            if submitted:
                options = [o.strip() for o in options_input.split('\n') if o.strip()]
                if len(options) < 2:
                    st.error("Need 2+ options")
                else:
                    st.session_state.markets.append({
                        "id": str(uuid.uuid4()),
                        "question": question,
                        "options": options,
                        "votes": {opt: 0 for opt in options},
                        "resolution_date": str(date),
                        "resolved": False
                    })
                    st.success("Voting live!")
                    st.balloons()

# Display Leaderboard
st.markdown("<h2 style='text-align:center;color:#39ff14'>🏆 BETA LEADERBOARD</h2>", unsafe_allow_html=True)
update_leaderboard()
if st.session_state.leaderboard:
    for i, entry in enumerate(st.session_state.leaderboard):
        badge = "👑" if i == 0 else "💎" if i == 1 else "🥉" if i == 2 else "🔥"
        st.markdown(f"**{i+1}.** {entry['username']} — {entry['votes']} votes {badge}")
else:
    st.info("No votes yet. Be the first degen!")

# Markets
st.markdown("<h2 style='text-align:center;color:#ff00ff'>🗳️ BETA VOTING BATTLES</h2>", unsafe_allow_html=True)

if not st.session_state.markets:
    st.info("No battles yet. Admin launching soon...")
else:
    for market in st.session_state.markets:
        with st.container():
            st.markdown("<div class='market-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;color:#00ffff'>{market['question']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;color:#ff00ff'>Ends: {market['resolution_date']}</p>", unsafe_allow_html=True)

            total_votes = sum(market['votes'].values())
            cols = st.columns(len(market['options']))
            for idx, opt in enumerate(market['options']):
                with cols[idx]:
                    perc = (market['votes'][opt] / total_votes * 100) if total_votes > 0 else 0
                    st.markdown(f"<h2 style='text-align:center;color:#39ff14'>{opt}<br>{perc:.1f}%</h2>", unsafe_allow_html=True)
                    vote_cost = 10000  # Simulated cost in sim $DEDU
                    if st.button(f"🗳️ VOTE {opt}", key=f"vote_{market['id']}_{idx}", use_container_width=True):
                        if st.session_state.sim_dedu_balance >= vote_cost or st.session_state.votes_cast < 10:
                            market['votes'][opt] += 1
                            st.session_state.votes_cast += 1
                            if st.session_state.votes_cast <= 10:
                                st.success(f"Free test vote used! Voted {opt} 🔥")
                            else:
                                st.session_state.sim_dedu_balance -= vote_cost
                                st.success(f"Voted {opt}! (-10,000 sim $DEDU)")
                            st.balloons()
                            update_leaderboard()
                            st.rerun()
                        else:
                            st.error("Not enough simulated $DEDU! Wait for more free votes or reset.")

            st.markdown("</div>", unsafe_allow_html=True)

# Reset Button for Testing
if st.button("🔄 RESET MY BETA ACCOUNT (for testing)"):
    st.session_state.user_id = None
    st.session_state.sim_dedu_balance = 0
    st.session_state.votes_cast = 0
    st.rerun()

# Footer
st.markdown("""
<div style='text-align:center;margin-top:60px;padding:40px;background:rgba(0,10,30,0.6);border:2px solid #39ff14;border-radius:20px'>
    <h2 style='color:#ff00ff'>Pre-DICKTOR Beta</h2>
    <p style='color:#39ff14'>Simulator Mode | 1M sim $DEDU per user | 10 free votes | Real leaderboard</p>
    <p style='color:#b0ffb0'>Feedback welcome — help us build the ultimate degen voting platform!</p>
</div>
""", unsafe_allow_html=True)
