import streamlit as st
import os
from openai import OpenAI
import random
import time

# Determine if we're running in a Streamlit Cloud environment
is_streamlit_cloud = os.environ.get('STREAMLIT_RUNTIME') == 'true'

if is_streamlit_cloud:
    # Use Streamlit secrets for production
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    # Use environment variable for local development
    api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Function to generate a riddle using OpenAI's GPT
@st.cache_data(ttl=0)
def generate_riddle():
    st.write("Generating riddle...")
    timestamp = int(time.time())
    random_word = random.choice(['mysterious', 'puzzling', 'enigmatic', 'perplexing', 'baffling'])
    prompt = f"Create a {random_word} riddle that's not commonly known. Be creative and unique. Timestamp: {timestamp}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        n=1,
        temperature=0.9,
    )
    riddle = response.choices[0].message.content.strip()
    return riddle

# Function to get the answer to the riddle
def get_riddle_answer(riddle):
    prompt = f"What is the answer to the riddle: {riddle}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30,
        n=1,
        temperature=0,
    )
    answer = response.choices[0].message.content.strip().lower()
    return answer

# Function to log the riddle game results
def log_riddle_game(riddle, correct_answer, user_guess, is_correct):
    """
    Log the riddle game results.
    """
    print(f"Riddle: {riddle}")
    print(f"Correct Answer: {correct_answer}")
    print(f"User Guess: {user_guess}")
    print(f"Is Correct: {is_correct}")
    print("---")

# Initialize session state variables to keep track of riddle, answer, and feedback
if 'riddle' not in st.session_state:
    st.session_state['riddle'] = ''
if 'answer' not in st.session_state:
    st.session_state['answer'] = ''
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = ''

# Set the title of the app
st.title("Riddle game time!")

# Generate a new riddle if there isn't one already
if not st.session_state['riddle']:
    st.session_state['riddle'] = generate_riddle()
    st.session_state['answer'] = get_riddle_answer(st.session_state['riddle'])
    st.session_state['feedback'] = ''

# Display the riddle to the user
st.write("### Riddle:")
st.write(st.session_state['riddle'])

# Create a form for the user input and submission
with st.form(key='riddle_form'):
    user_answer = st.text_input("Your Answer:")
    submit_button = st.form_submit_button("Submit Answer")

# When the form is submitted (either by clicking the button or pressing Enter)
if submit_button:
    if user_answer:
        # Check if the user's answer matches or is contained within the correct answer
        is_correct = user_answer.strip().lower() in st.session_state['answer']
        if is_correct:
            st.session_state['feedback'] = "Correct! Well done."
        else:
            st.session_state['feedback'] = f"Incorrect. {st.session_state['answer'].capitalize()}"
        
        # Log the riddle game results
        log_riddle_game(
            st.session_state['riddle'],
            st.session_state['answer'],
            user_answer.strip().lower(),
            is_correct
        )
    else:
        st.session_state['feedback'] = "Please enter an answer."

# Display feedback based on the user's answer
if st.session_state['feedback']:
    if "Correct" in st.session_state['feedback']:
        st.success(st.session_state['feedback'])
    elif "Incorrect" in st.session_state['feedback']:
        st.error(st.session_state['feedback'])
    else:
        st.warning(st.session_state['feedback'])

# Add a visual separator
st.divider()

# Provide an option to solve another riddle
if st.button("Solve Another Riddle"):
    # Reset the session state to generate a new riddle
    st.session_state['riddle'] = ''
    st.session_state['answer'] = ''
    st.session_state['feedback'] = ''
    # Rerun the app to update the state
    st.rerun()
