import streamlit as st
import random
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Manually enter Google service account credentials
service_account_info = {
  "type": "service_account",
  "project_id": "velvety-folder-403710",
  "private_key_id": "48e75b97c08e6e57ea6d7436a40d4c8ebb39bb68",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDiCKCp85EyvjF3\nVBt7gSbT0LzCD/zU+TimjGmQ9JR/NYOz5YcuibfrlxlhPqTY98HofduKO6TdbOqw\nxs7lgF/OEQT5yj3f04EygfuZxzxRJSPx1KPTka3uRENC01BZjEvw5QKP2LmwMsom\neUNIjYpYrOcW/Fdq3rTOT5vKrtIVk7b4O4NmpaqvfNyW4mdaXuc2d7GJH54VDaJX\nmj8XihsUw6B0V4V7IzeNh5SLFWln5mTj5pRz4P4GxHm5oHTh6fK/WHaS6hVb1hE6\nlVOxawgPFvOveZu7VN8VLSWjTOycUycm69JvciqEBlgupyUFSF03vPm5aCCjBZVP\nTZ0uirZZAgMBAAECggEAHuCVggyXKIVkIIGe13pHIZGsQh5eUtb7btT+Ps0KfsOC\ntaUvQvjmj7UDxI2the4ie8NlpYvhnlXt9tl8aKGRdNxM/7Upn//hRahirxkmcOH6\nomMtQLjv4lKflZYPAzdFJdKYTP+K2OUMnxYwTiL3uTFgHXsPPgwk9YyueDugJfjW\noSmptoAyhPObepgQaUk5xaQorvzf93lQUiFN8hbouVwdJbGDTGLUJmfn6wS7IcKy\n42CWhyY7bjDfWA8nTNLbpP2QkksNhmifGnYX3LkOAfJ+pAPM2lVE3muOSNcRT5b7\nvniWApBXvDKuVgSKGlDbyyhpkcwuURHfMEsjAn4u2QKBgQD//278+DyKOqBViJvp\nWgcXu1SNAoTboAHzJXQI00q78BqGcQCqYEyB0UuzmbzRfUUlrtjaPw/g2OObPRXd\nVv08qwl0HEBm8jjjB8ZLcjfp6q0AkZeS7OP/nCM2uCWk02/WbAz8na+1GmSd4u9N\nR44Mj7/LFOmmcr8ahU1eQbum/wKBgQDiCSCzzA1AQlv9sxInamvQz0jIg1G4XN//\nUMGmvOSvB4vOVmq/ozuAOkdACrNeQVpyVSbpn8JEJsJX1dt+20Cm/E/D/1Z5vLm2\nhtfjKiWP3SQkdPN9lXn9KcMEWnaKfLjSy3vwx68jmM0jcpUCwuxyvaOQcy9EL1EX\nKPIQSbU6pwKBgQCzXOcIu2y/dQAtrb9/qiJaEFjXS7KGpv92uwEnxdMRBtOu6rIK\nrdotAtXFiqvvI5Q1KOKrV4/qfExM0mnlYTOhND01ay38cy5Ec4gOCIMAk/qO8XN/\n8BZ3W5CYoEFP0Q0E8UPQIzOe8lUZAo2kWcQ/LOC2i3qBstgO3uMsbWXrRQKBgQC5\nNquCSHCPOBDy2HnGrHA+AKvuCZS70faF2eFkRCHKvg8z+yGreBC4aIiblGkXkcuQ\nJfAlvQ/NEklq+cTKtNPMQLEHtEFirV8rjmB2NsHimV0VNnOScxordL3k4k+B+OLl\nb3FWgfkj3QAyzKAHTDu9ZWESax/O6kqzBI0dBZinvwKBgBKj5SBbbkw+xETl5R+Q\nceApCPPcHx4apMiTnHQTQJZiWHuJ31ml4Y57RU3fe4T3GTEstd7W6Ee5oumxNcMl\nxrSuvRPTEM+KB91hKG8SNc5k+HEIRASBEHQbW9AH/FVmM9Nu27fUmo3PyFSKHFDS\nkbA75ylCAOJxOGS9KirtYifl\n-----END PRIVATE KEY-----\n",
  "client_email": "streamlit-auction-service@velvety-folder-403710.iam.gserviceaccount.com",
  "client_id": "114197490509524914433",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-auction-service%40velvety-folder-403710.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open("Player Auction").sheet1

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

# Load sold players and team budgets from Google Sheets
def load_data():
    data = sheet.get_all_records()
    sold_players = {row["Player"]: {"Team": row["Team"], "Bid": float(row["Bid"])} for row in data}
    return sold_players

st.title("🏏 Cricket Player Auction Dashboard")

# Load sold players
sold_players = load_data()

# Category Selection
category = st.selectbox("Select a category", list(players.keys()))

# Get unsold players from the selected category
unsold_players = [p for p in players[category] if p not in sold_players]

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
            # Save data to Google Sheets
            sheet.append_row([selected_player, team_name, bid_amount])
            st.success(f"✅ {selected_player} sold to {team_name} for {bid_amount} crore!")
            st.session_state.current_player = None  # Reset current player for the next auction
            st.experimental_rerun()
        else:
            st.error("⚠️ Please select a valid team before selling the player.")
else:
    st.warning(f"⚠️ All players in **{category}** have been sold.")

# Display sold players in a table
st.subheader("🏆 Sold Players")
if sold_players:
    sold_df = pd.DataFrame([{"Player": k, "Team": v["Team"], "Bid": v["Bid"]} for k, v in sold_players.items()])
    st.dataframe(sold_df)
else:
    st.info("No players have been sold yet.")
