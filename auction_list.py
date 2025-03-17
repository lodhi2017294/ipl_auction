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

# Initialize session state for tracking sold players
if "sold_players" not in st.session_state:
    st.session_state.sold_players = {}
if "last_sold_player" not in st.session_state:
    st.session_state.last_sold_player = None

# Streamlit UI
st.title("🏏 Cricket Player Auction Dashboard")

# Category Selection
category = st.selectbox("Select a category", list(players.keys()))

# Get unsold players from the selected category
unsold_players = [p for p in players[category] if p not in st.session_state.sold_players]

# Auction Logic
if unsold_players:
    # Pick a random unsold player
    selected_player = random.choice(unsold_players)
    st.subheader(f"🟢 Player up for auction: **{selected_player}**")

    # Dropdown for team selection
    team_name = st.selectbox("Select the team buying this player:", teams)

    # Sell player button
    if st.button("Sell Player"):
        if team_name:  # Ensure a team is selected
            st.session_state.sold_players[selected_player] = team_name
            st.session_state.last_sold_player = selected_player
            st.success(f"✅ {selected_player} sold to {team_name}!")
            st.experimental_rerun()  # Refresh the page to pick next player
        else:
            st.error("⚠️ Please select a valid team before selling the player.")
else:
    st.warning(f"⚠️ All players in **{category}** have been sold.")

# Display last sold player to avoid re-selection issue
if st.session_state.last_sold_player:
    st.write(f"**Last sold player:** {st.session_state.last_sold_player}")

# Display sold players in a table
st.subheader("🏆 Sold Players")
if st.session_state.sold_players:
    sold_df = pd.DataFrame(list(st.session_state.sold_players.items()), columns=["Player", "Team"])
    st.dataframe(sold_df)
else:
    st.info("No players have been sold yet.")
