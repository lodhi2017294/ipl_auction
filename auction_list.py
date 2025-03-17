import streamlit as st
import random
import pandas as pd

# Define player categories
players = {
    "Batters": [
        "Virat Kohli", "Rohit Sharma", "Ruturaj Gaikwad", "Shubman Gill", "Yashasvi Jaiswal",
        "Travis Head", "Shreyas Iyer", "Suryakumar Yadav", "Tilak Varma", "David Miller", "Rinku Singh"
    ],
    "Bowlers": [
        "Jasprit Bumrah", "Trent Boult", "Arshdeep Singh", "Yuzvendra Chahal", "Kuldeep Yadav",
        "Mitchell Starc", "Bhuvneshwar Kumar", "Josh Hazlewood", "Mohammed Shami", "Varun Chakravarthy",
        "Jofra Archer", "Matheesha Pathirana"
    ],
    "Bowling All-rounders": [
        "Ravindra Jadeja", "Ravichandran Ashwin", "Sam Curran", "Sunil Narine", "Axar Patel",
        "Pat Cummins", "Marco Jansen", "Mitchell Santner", "Rashid Khan", "Washington Sundar"
    ],
    "Batting All-rounders": [
        "Mitchell Marsh", "Glenn Phillips", "Hardik Pandya", "Glenn Maxwell", "Marcus Stoinis",
        "Liam Livingstone", "Nitish Reddy", "Abhishek Sharma", "Venkatesh Iyer", "Andre Russell",
        "Moeen Ali", "Rachin Ravindra", "Shivam Dube"
    ],
    "Wicketkeepers": [
        "MS Dhoni", "Heinrich Klaasen", "Sanju Samson", "Quinton de Kock", "Ishan Kishan",
        "Philip Salt", "KL Rahul", "Tristan Stubbs", "Jos Buttler", "Nicholas Pooran", "Rishabh Pant"
    ]
}

# Allowed Teams
teams = ["Vishal", "Vaibhav", "Vishnu", "Jaggu"]

# Initialize session state for tracking sold players and team budgets
if "sold_players" not in st.session_state:
    st.session_state.sold_players = {}
if "team_budget" not in st.session_state:
    st.session_state.team_budget = {team: 120 for team in teams}  # 120 crore per team

st.title("🏏 Cricket Player Auction Dashboard")

# Category Selection
category = st.selectbox("Select a category", list(players.keys()))

# Get unsold players from the selected category
unsold_players = [p for p in players[category] if p not in st.session_state.sold_players]

if unsold_players:
    # Pick a random unsold player
    selected_player = random.choice(unsold_players)
    st.subheader(f"🟢 Player up for auction: **{selected_player}**")

    # Dropdown for team selection
    team_name = st.selectbox("Select the team buying this player:", teams)

    # Input for bid amount
    bid_amount = st.number_input("Enter bid amount (in crores):", min_value=1, max_value=120, step=1)

    # Sell player button
    if st.button("Sell Player"):
        if team_name and selected_player and bid_amount <= st.session_state.team_budget[team_name]:
            # Deduct amount from team's budget
            st.session_state.team_budget[team_name] -= bid_amount
            st.session_state.sold_players[selected_player] = {"Team": team_name, "Bid": bid_amount}
            st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
            st.experimental_rerun()  # Refresh the page to pick next player
        else:
            st.error("⚠️ Invalid bid amount or insufficient budget!")
else:
    st.warning(f"⚠️ All players in **{category}** have been sold.")

# Display team budgets
st.subheader("💰 Team Budgets")
budget_df = pd.DataFrame(st.session_state.team_budget.items(), columns=["Team", "Remaining Budget (crores)"])
st.dataframe(budget_df)

# Display sold players in a table
st.subheader("🏆 Sold Players")
if st.session_state.sold_players:
    sold_df = pd.DataFrame([{**{"Player": k}, **v} for k, v in st.session_state.sold_players.items()])
    st.dataframe(sold_df)
else:
    st.info("No players have been sold yet.")
