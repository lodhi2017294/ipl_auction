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

# Allowed Teams and initial purse
teams = {"Vishal": 120.0, "Vaibhav": 120.0, "Vishnu": 120.0, "Jaggu": 120.0}

# Reset session state on refresh
if not st.session_state.get("initialized", False):
    st.session_state.sold_players = {team: [] for team in teams.keys()}
    st.session_state.team_budgets = teams.copy()
    st.session_state.remaining_players = {cat: list(players[cat]) for cat in players}
    st.session_state.initialized = True

st.set_page_config(layout="wide")
st.title("🏏 Cricket Player Auction Dashboard")

# Layout setup
header_col1, header_col2, header_col3 = st.columns([3, 2, 3])

with header_col1:
    st.subheader("🏆 Sold Players by Team")
    sold_players_data = {team: [] for team in teams.keys()}
    for team, players_sold in st.session_state.sold_players.items():
        sold_players_data[team] = players_sold
    
    sold_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in sold_players_data.items()]))
    st.dataframe(sold_df.fillna("-"), width=800)

with header_col2:
    st.subheader("💰 Remaining Purse of Teams")
    budget_df = pd.DataFrame(st.session_state.team_budgets.items(), columns=["Team", "Remaining Budget (crores)"])
    st.dataframe(budget_df, width=700)

with header_col3:
    category = st.selectbox("Select a category", list(players.keys()))
    next_player_button = st.button("Next Player ➡️", key="next_player_button")

col1, col2 = st.columns([3, 2])

with col1:
    # Get unsold players from the selected category
    unsold_players = st.session_state.remaining_players[category]

    if "current_player" not in st.session_state or next_player_button:
        if unsold_players:
            st.session_state.current_player = random.choice(unsold_players)
        else:
            st.session_state.current_player = None

    if st.session_state.current_player:
        selected_player = st.session_state.current_player
        st.subheader(f"🟢 Player up for auction: **{selected_player}**")

        # Dropdown for team selection
        team_name = st.selectbox("Select the team buying this player:", list(st.session_state.team_budgets.keys()))

        # Input for bid amount (decimal values allowed)
        bid_amount = st.number_input("Enter bid amount (in crores):", min_value=0.1, max_value=st.session_state.team_budgets[team_name], step=0.1)

        # Sell player button
        if st.button("Sell Player ✅", key="sell_button"):
            if team_name and bid_amount <= st.session_state.team_budgets[team_name]:
                # Save data to session state
                st.session_state.sold_players[team_name].append(f"{selected_player} ({bid_amount} cr)")
                st.session_state.team_budgets[team_name] -= bid_amount  # Deduct from team budget
                
                # Remove the player from the remaining players list
                for cat in st.session_state.remaining_players:
                    if selected_player in st.session_state.remaining_players[cat]:
                        st.session_state.remaining_players[cat].remove(selected_player)
                        break
                
                st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
                st.session_state.current_player = None  # Reset current player for the next auction
                st.rerun()
            else:
                st.error("⚠️ Please select a valid team before selling the player.")
    elif len(unsold_players) == 0:
        st.warning(f"⚠️ All players in **{category}** have been sold.")

    if all(len(team) == 0 for team in st.session_state.sold_players.values()) and all(len(p) == 0 for p in st.session_state.remaining_players.values()):
        st.success("🎉 All marquee players have been auctioned! No more players left.")

with col2:
    # Display remaining players category-wise
    st.subheader("📋 Remaining Players")
    remaining_players_data = {cat: st.session_state.remaining_players[cat] for cat in st.session_state.remaining_players}
    remaining_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in remaining_players_data.items()]))
    st.dataframe(remaining_df.fillna("-"), width=800)
