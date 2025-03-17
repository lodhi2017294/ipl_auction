import streamlit as st
import random
import pandas as pd

# Define the player categories
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

# Load or initialize auction state
if "sold_players" not in st.session_state:
    st.session_state.sold_players = {}

st.title("🏏 Cricket Player Auction Dashboard")

# Select category
category = st.selectbox("Select a category", list(players.keys()))

# Filter unsold players
unsold_players = [p for p in players[category] if p not in st.session_state.sold_players]

if unsold_players:
    # Pick a random unsold player
    selected_player = random.choice(unsold_players)
    st.subheader(f"🟢 Player up for auction: {selected_player}")
    
    # Enter team name
    team_name = st.text_input("Enter the team buying this player:")
    
    if st.button("Sell Player"):
        if team_name:
            st.session_state.sold_players[selected_player] = team_name
            st.success(f"✅ {selected_player} sold to {team_name}!")
            st.experimental_rerun()
        else:
            st.error("⚠️ Please enter a team name before selling the player.")
else:
    st.warning(f"All players in {category} have been sold.")

# Display auction results
st.subheader("🏆 Sold Players")
sold_df = pd.DataFrame(list(st.session_state.sold_players.items()), columns=["Player", "Team"])
st.dataframe(sold_df)
