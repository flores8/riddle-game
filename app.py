import weave
import streamlit as st
import openai
import os

weave.init("wandb-designers/riddle-game")

# Determine if we're running in a Streamlit Cloud environment
is_streamlit_cloud = os.environ.get('STREAMLIT_RUNTIME') == 'true'

if is_streamlit_cloud:
    # Use Streamlit secrets for production
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    # Use environment variable for local development
    api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a riddle using OpenAI's GPT
def generate_riddle():
    # Prompt for the AI
    prompt = "Tell me a riddle."
    # Call the OpenAI API to get a response
    response = openai.Completion.create(
        engine="text-davinci-003",  # Using the GPT-3 model
        prompt=prompt,
        max_tokens=60,              # Limit the response tokens
        n=1,                        # Number of responses to generate
        stop=None,
        temperature=0.7,            # Controls the randomness of the output
    )
    # Extract the riddle from the response
    riddle = response.choices[0].text.strip()
    return riddle

# Function to get the answer to the riddle
def get_riddle_answer(riddle):
    # Prompt to ask for the answer to the riddle
    prompt = f"What is the answer to the riddle: {riddle}"
    # Call the OpenAI API to get the answer
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=30,
        n=1,
        stop=None,
        temperature=0,
    )
    # Extract the answer and convert it to lowercase for comparison
    answer = response.choices[0].text.strip().lower()
    return answer

# Initialize session state variables to keep track of riddle, answer, and feedback
if 'riddle' not in st.session_state:
    st.session_state['riddle'] = ''
if 'answer' not in st.session_state:
    st.session_state['answer'] = ''
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = ''

# Set the title of the app
st.title("AI-Based Trivia Quiz Master")

# Generate a new riddle if there isn't one already
if not st.session_state['riddle']:
    st.session_state['riddle'] = generate_riddle()
    st.session_state['answer'] = get_riddle_answer(st.session_state['riddle'])
    st.session_state['feedback'] = ''

# Display the riddle to the user
st.write("### Riddle:")
st.write(st.session_state['riddle'])

# Input field for the user to submit their answer
user_answer = st.text_input("Your Answer:")

# When the user clicks the "Submit Answer" button
if st.button("Submit Answer"):
    if user_answer:
        # Check if the user's answer matches or is contained within the correct answer
        if user_answer.strip().lower() in st.session_state['answer']:
            st.session_state['feedback'] = "Correct! Well done."
        else:
            st.session_state['feedback'] = f"Incorrect. The correct answer was: {st.session_state['answer'].capitalize()}"
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

# Provide an option to solve another riddle
if st.button("Solve Another Riddle"):
    # Reset the session state to generate a new riddle
    st.session_state['riddle'] = ''
    st.session_state['answer'] = ''
    st.session_state['feedback'] = ''
    # Rerun the app to update the state
    st.experimental_rerun()
