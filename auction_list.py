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

# Initialize session state for sold players
if "sold_players" not in st.session_state:
    st.session_state.sold_players = {}

st.title("🏏 Cricket Player Auction Dashboard")

# Category Selection
category = st.selectbox("Select a category", list(players.keys()))

# Get unsold players from the selected category
unsold_players = [p for p in players[category] if p not in st.session_state.sold_players]

if "current_player" not in st.session_state or st.button("Next Player ➡️"):
    if unsold_players:
        st.session_state.current_player = random.choice(unsold_players)
    else:
        st.session_state.current_player = None

if st.session_state.current_player:
    selected_player = st.session_state.current_player
    st.subheader(f"🟢 Player up for auction: **{selected_player}**")

    # Dropdown for team selection
    team_name = st.selectbox("Select the team buying this player:", teams)

    # Input for bid amount (decimal values allowed)
    bid_amount = st.number_input("Enter bid amount (in crores):", min_value=0.1, max_value=120.0, step=0.1)

    # Sell player button
    if st.button("Sell Player ✅"):
        if team_name:
            # Save data to session state
            st.session_state.sold_players[selected_player] = {"Team": team_name, "Bid": bid_amount}
            st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
            st.session_state.current_player = None  # Reset current player for the next auction
            st.rerun()
        else:
            st.error("⚠️ Please select a valid team before selling the player.")
else:
    st.warning(f"⚠️ All players in **{category}** have been sold.")

# Display sold players in a table
st.subheader("🏆 Sold Players")
if st.session_state.sold_players:
    sold_df = pd.DataFrame([{"Player": k, "Team": v["Team"], "Bid": v["Bid"]} for k, v in st.session_state.sold_players.items()])
    st.dataframe(sold_df)
else:
    st.info("No players have been sold yet.")
