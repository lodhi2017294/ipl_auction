import streamlit as st
import random
import pandas as pd
import os

# File Path in the Streamlit Cloud (inside the connected GitHub repo)
CSV_FILE_PATH = "final_updated.csv"  # Ensure this file exists in the same directory

# Function to load CSV and process data
def load_player_data():
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH)
        return df
    else:
        st.error("⚠️ CSV file not found. Please check the file path!")
        return pd.DataFrame()

# Load player data from CSV
df = load_player_data()

# Extract sold players from the CSV
sold_players = set(df.values.flatten())  # Extract all sold player names from the CSV

# Define player categories with available players only
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

# Remove sold players from the list
remaining_players = {
    category: [player for player in player_list if player not in sold_players]
    for category, player_list in players.items()
}

# Allowed Teams and initial purse
teams = {"Vishal": 120.0, "Vaibhav": 120.0, "Vishnu": 120.0}

# Initialize session state if not done
if not st.session_state.get("initialized", False):
    st.session_state.sold_players = {team: [] for team in teams.keys()}
    st.session_state.team_budgets = teams.copy()
    st.session_state.remaining_players = remaining_players
    st.session_state.initialized = True

st.set_page_config(layout="wide")
st.title("🏏 Cricket Player Auction Dashboard")

# Layout setup
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🏆 Sold Players by Team (Editable)")
    sold_players_data = {team: [] for team in teams.keys()}
    for team, players_sold in st.session_state.sold_players.items():
        sold_players_data[team] = players_sold

    sold_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in sold_players_data.items()]))
    edited_sold_df = st.data_editor(sold_df.fillna("-"), width=900)

    st.subheader("📋 Remaining Players")
    remaining_df = pd.DataFrame({cat: pd.Series(players) for cat, players in st.session_state.remaining_players.items()})
    st.dataframe(remaining_df.fillna("-"), width=900)

with col2:
    st.subheader("💰 Remaining Purse of Teams (Editable)")
    budget_df = pd.DataFrame(st.session_state.team_budgets.items(), columns=["Team", "Remaining Budget (crores)"])
    edited_budget_df = st.data_editor(budget_df, width=600)
    st.session_state.team_budgets = dict(zip(edited_budget_df["Team"], edited_budget_df["Remaining Budget (crores)"]))

    category = st.selectbox("Select a category", list(players.keys()))
    next_player_button = st.button("Next Player ➡️", key="next_player_button")

    unsold_players = st.session_state.remaining_players[category]
    if "current_player" not in st.session_state or next_player_button:
        if unsold_players:
            st.session_state.current_player = random.choice(unsold_players)
        else:
            st.session_state.current_player = None

    if st.session_state.current_player:
        selected_player = st.session_state.current_player
        st.subheader(f"🟢 Player up for auction: **{selected_player}**")

        team_name = st.selectbox("Select the team buying this player:", list(st.session_state.team_budgets.keys()))
        bid_amount = st.number_input("Enter bid amount (in crores):", min_value=0.1, max_value=st.session_state.team_budgets[team_name], step=0.1)

        if st.button("Sell Player ✅", key="sell_button"):
            if team_name and bid_amount <= st.session_state.team_budgets[team_name]:
                # Add player to sold list
                st.session_state.sold_players[team_name].append(f"{selected_player} ({bid_amount} cr)")
                st.session_state.team_budgets[team_name] -= bid_amount

                # Remove player from remaining list
                for cat in st.session_state.remaining_players:
                    if selected_player in st.session_state.remaining_players[cat]:
                        st.session_state.remaining_players[cat].remove(selected_player)
                        break

                # Update CSV with new sold player
                df.loc[len(df)] = [selected_player]
                df.to_csv(CSV_FILE_PATH, index=False)

                st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
                st.session_state.current_player = None
                st.rerun()
            else:
                st.error("⚠️ Please select a valid team before selling the player.")
    elif len(unsold_players) == 0:
        st.warning(f"⚠️ All players in **{category}** have been sold.")

    if all(len(team) == 0 for team in st.session_state.sold_players.values()) and all(len(p) == 0 for p in st.session_state.remaining_players.values()):
        st.success("🎉 All marquee players have been auctioned! No more players left.")

