import streamlit as st
import random

if 'level' not in st.session_state:
    st.session_state.level = 1  

# Sidebar Difficulty Selector
st.session_state.level = st.sidebar.slider(
    "*Select a difficulty level*", 1, 3, st.session_state.level
)

# Set  difficulty level
if st.session_state.level == 1:
    endRange = 10
elif st.session_state.level == 2:
    endRange = 50
elif st.session_state.level == 3:
    endRange = 100

if 'game_started' not in st.session_state:
    st.session_state.game_started = False 

if 'random_num' not in st.session_state or st.session_state.game_started == False:
    st.session_state.random_num = random.randint(1, endRange)

if 'num_of_attempts' not in st.session_state:
    st.session_state.num_of_attempts = []

def load_css(file_name="styles.css"):
    with open(file_name, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

if not st.session_state.game_started:
    st.title("🎮 Welcome to the Number Guessing Game!")
    st.write("Click 'Start Game' to begin.")

    if st.button("Start Game"):
        st.session_state.game_started = True  
        st.session_state.random_num = random.randint(1, endRange)  
        st.session_state.num_of_attempts = []  
        st.rerun()  

# Game interface
if st.session_state.game_started:
    st.title("Guess The Number")
    game_over = len(st.session_state.num_of_attempts) >= 10

    st.write(f"Attempts: {len(st.session_state.num_of_attempts)}/10")

    guessed_number = st.number_input(
        f"Guess the number between 1 to {endRange}", 1, endRange, key="guess", disabled=game_over
    )
    def show_success(message):
        st.markdown(f'<div class="custom-success">🎉 {message}</div>', unsafe_allow_html=True)

    def show_warning(message):
        st.markdown(f'<div class="custom-warning">⚠️ {message}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Guess", disabled=game_over):
            if guessed_number == st.session_state.random_num :
                show_success(f"Correct! You guessed it in {len(st.session_state.num_of_attempts) + 1} attempts.")
            elif guessed_number < st.session_state.random_num:
                show_warning("Too low! Try again.")
            else:
                show_warning("Too high! Try again.")

            st.session_state.num_of_attempts.append(guessed_number)

        if game_over:
            st.markdown('<div class="game-over">❌ Game Over! You\'ve reached 10 attempts.</div>', unsafe_allow_html=True)


            st.write(f"The correct number was: {st.session_state.random_num}")

    with col2:
        if st.button("Restart Game"):
            st.session_state.game_started = False 
            st.session_state.random_num = random.randint(1, endRange)  
            st.session_state.num_of_attempts = []  
            st.rerun()  