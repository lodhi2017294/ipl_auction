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
    st.session_state.initialized = True

st.set_page_config(layout="wide")
st.title("🏏 Cricket Player Auction Dashboard")

# Full-width layout
col1, col2 = st.columns([3, 2])

with col1:
    # Category Selection
    category = st.selectbox("Select a category", list(players.keys()))

    # Get unsold players from the selected category
    unsold_players = [p for p in players[category] if not any(p in team for team in st.session_state.sold_players.values())]

    if "current_player" not in st.session_state or st.button("Next Player ➡️"):
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
        if st.button("Sell Player ✅"):
            if team_name and bid_amount <= st.session_state.team_budgets[team_name]:
                # Save data to session state
                st.session_state.sold_players[team_name].append(f"{selected_player} ({bid_amount} cr)")
                st.session_state.team_budgets[team_name] -= bid_amount  # Deduct from team budget
                st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
                st.session_state.current_player = None  # Reset current player for the next auction
                st.rerun()
            else:
                st.error("⚠️ Please select a valid team before selling the player.")
    elif len(unsold_players) == 0:
        st.warning(f"⚠️ All players in **{category}** have been sold.")

    # Display remaining players category-wise
    st.subheader("📋 Remaining Players")
    for cat, cat_players in players.items():
        remaining = [p for p in cat_players if not any(p in team for team in st.session_state.sold_players.values())]
        if remaining:
            st.write(f"**{cat}**: {', '.join(remaining)}")
        else:
            st.write(f"**{cat}**: ✅ All players sold!")

with col2:
    # Display remaining team budgets
    st.subheader("💰 Remaining Purse of Teams")
    budget_df = pd.DataFrame(st.session_state.team_budgets.items(), columns=["Team", "Remaining Budget (crores)"])
    st.dataframe(budget_df, width=700)

    # Display sold players categorized by team
    st.subheader("🏆 Sold Players by Team")
    team_columns = st.columns(4)  # Create 4 columns for each team
    
    for idx, (team, players_sold) in enumerate(st.session_state.sold_players.items()):
        with team_columns[idx]:
            st.write(f"### {team}")
            if players_sold:
                for player in players_sold:
                    st.write(f"- {player}")
            else:
                st.write("No players sold yet.")
