# FIX: Updated import to use check_guess from logic_utils.py using Copilot Agent Mode
import random
import streamlit as st
from logic_utils import check_guess
import os

# AGENT: Implemented High Score Tracker using Copilot Agent Mode
# Load high score from file
HIGH_SCORE_FILE = "high_score.txt"
if os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "r") as f:
        try:
            high_score = int(f.read().strip())
        except ValueError:
            high_score = 0
else:
    high_score = 0


def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Reject decimal numbers
    if "." in raw:
        return False, None, "Decimal numbers are not allowed."

    # Reject non-numeric input
    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # Reject negative or zero values
    if value <= 0:
        return False, None, "Enter a positive number."

    # Reject out-of-range guesses
    if value < low or value > high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Ensure the secret is always within the current difficulty range
if "secret" not in st.session_state or not (low <= st.session_state.secret <= high):
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Display high score in sidebar
st.sidebar.subheader("High Score")
st.sidebar.write(f"Best Score: {high_score}")

# AGENT: Implemented Guess History Sidebar using Copilot Agent Mode
st.sidebar.subheader("Guess History")
if st.session_state.history:
    for guess, outcome in st.session_state.history:
        st.sidebar.write(f"Guess: {guess} - {outcome}")
else:
    st.sidebar.write("No guesses yet.")

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# Reset all game state when starting a new game
if new_game:
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append((raw_guess, "Invalid"))
        st.error(err)
    else:
        st.session_state.history.append((guess_int, "Pending"))  # temporary

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Update history with outcome
        st.session_state.history[-1] = (guess_int, outcome)

        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(message)
            elif outcome == "Too Low":
                st.info(message)

            # Hot/Cold feedback
            distance = abs(guess_int - st.session_state.secret)
            if distance <= 3:
                st.write("🔥 Hot!")
            elif distance <= 10:
                st.write("🌡️ Warm!")
            else:
                st.write("❄️ Cold!")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            # Update high score if beaten
            if st.session_state.score > high_score:
                high_score = st.session_state.score
                with open(HIGH_SCORE_FILE, "w") as f:
                    f.write(str(high_score))

            # Game Summary Table
            st.subheader("Game Summary")
            summary_data = {
                "Metric": ["Total Attempts", "Final Score"],
                "Value": [st.session_state.attempts, st.session_state.score]
            }
            st.table(summary_data)

            st.subheader("Guess History")
            history_data = [{"Guess": guess, "Outcome": outcome} for guess, outcome in st.session_state.history]
            st.table(history_data)
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
