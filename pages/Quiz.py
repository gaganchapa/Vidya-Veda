import json
import streamlit as st
from typing import Dict
from langchain_ai21 import ChatAI21
from langchain_core.prompts import PromptTemplate
import os

# Initialize API key for AI21
os.environ["AI21_API_KEY"] = "lLYViWulXPnnL8i3i6UnhePluelfH9S1"
llm = ChatAI21(model="j2-ultra", max_tokens=2048)

# Define the prompt template
template1 = """
You are an AI Quiz Master.
Previous conversation:
{chat_history}
New human question: {question}
Response:
"""

prompt = PromptTemplate(
    template=template1,
    input_variables=['question', 'chat_history']
)

chain = prompt | llm

# Initialize chat history
chat_history = [
    {
        "role": "system",
        "content": "You are a REST API server with an endpoint /generate-random-question/:topic, which generates unique random quiz question in json data.",
    },
    {"role": "user", "content": "GET /generate-random-question/devops"},
    {
        "role": "assistant",
        "content": '''
        {
            "question": "What is the difference between Docker and Kubernetes?",
            "options": ["Docker is a containerization platform whereas Kubernetes is a container orchestration platform", "Kubernetes is a containerization platform whereas Docker is a container orchestration platform", "Both are containerization platforms", "Neither are containerization platforms"],
            "answer": "Docker is a containerization platform whereas Kubernetes is a container orchestration platform",
            "explanation": "Docker helps you create, deploy, and run applications within containers, while Kubernetes helps you manage collections of containers, automating their deployment, scaling, and more."
        }
        ''',
    },
    {"role": "user", "content": "GET /generate-random-question/jenkins"},
    {
        "role": "assistant",
        "content": '''
        {
            "question": "What is Jenkins?",
            "options": ["A continuous integration server", "A database management system", "A programming language", "An operating system"],
            "answer": "A continuous integration server",
            "explanation": "Jenkins is an open source automation server that helps to automate parts of the software development process such as building, testing, and deploying code."
        }
        ''',
    },
]

# Function to get a quiz question from a given topic
def get_quiz_from_topic(topic: str) -> Dict[str, str]:
    global chat_history
    # Create a copy of chat history to avoid modifying the global one
    current_chat = chat_history[:]
    current_user_message = {
        "role": "user",
        "content": f"GET /generate-random-question/{topic}",
    }
    current_chat.append(current_user_message)
    
    # Format chat history as a string
    formatted_chat_history = "\n".join([json.dumps(msg) for msg in current_chat])
    
    # Generate the quiz using the LLM chain
    response = chain.invoke({
        'question': f"GET /generate-random-question/{topic}",
        'chat_history': formatted_chat_history
    })
    
    # Extract the content from the AIMessage object
    quiz = response.content  # Assuming response is an AIMessage object with 'content' attribute
    
    # Add the assistant's response to the chat history
    current_assistant_message = {"role": "assistant", "content": quiz}
    chat_history.append(current_assistant_message)
    
    # Clean up the response and return the JSON data
    import re
    quiz = re.sub(r'```json|```', '', quiz).strip()

    # Debug print statement to inspect the quiz content
    print(f"Quiz Content: {quiz}")

    try:
        json_string = json.loads(quiz)
        if not all(key in json_string for key in ['question', 'options', 'answer', 'explanation']):
            raise ValueError("Missing required keys in the response JSON")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error decoding JSON or missing keys: {e}")
        json_string = {}

    return json_string
f = open("user_data.txt", "r")
main = f.readline()
sub = f.readline()
q = f"{main}  {sub}"
# Streamlit UI
topic = st.sidebar.text_input(
    "To change topic just enter below. From next new quiz question the topic entered here will be used.",
    value=q,
)

# Initialize session state variables if they don't exist yet
if "current_question" not in st.session_state:
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.right_answers = 0
    st.session_state.wrong_answers = 0

# Function to display the current question and options
def display_question():
    if len(st.session_state.questions) == 0:
        first_question = get_quiz_from_topic(topic)
        if first_question:
            st.session_state.questions.append(first_question)
        else:
            st.write("Failed to fetch the first question. Please try again.")

    if len(st.session_state.questions) == 0:
        return

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = st.session_state.current_question in st.session_state.answers

    # Get the current question from the questions list
    question = st.session_state.questions[st.session_state.current_question]

    # Display the question prompt
    st.write(f"{st.session_state.current_question + 1}. {question['question']}")

    # Use an empty placeholder to display the radio button options
    options = st.empty()

    # Display the radio button options and wait for the user to select an answer
    user_answer = options.radio("Your answer:", question["options"], key=st.session_state.current_question)

    # Display the submit button and disable it if necessary
    submit_button = st.button("Submit", disabled=submit_button_disabled)

    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]
        options.radio(
            "Your answer:",
            question["options"],
            key=f"answered_{st.session_state.current_question}",
            index=index,
        )

    if submit_button:
        st.session_state.answers[st.session_state.current_question] = question["options"].index(user_answer)

        if user_answer == question["answer"]:
            st.write("Correct!")
            st.session_state.right_answers += 1
        else:
            st.write(f"Sorry, the correct answer was {question['answer']}.")
            st.session_state.wrong_answers += 1

        with st.expander("Explanation"):
            st.write(question["explanation"])

    st.success(f"Right answers: {st.session_state.right_answers}")
    st.warning(f"Wrong answers: {st.session_state.wrong_answers}")

# Function to go to the next question
def next_question():
    st.session_state.current_question += 1
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        next_question = get_quiz_from_topic(topic)
        if next_question:
            st.session_state.questions.append(next_question)

# Function to go to the previous question
def prev_question():
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1

# Create a 3-column layout for the Prev/Next buttons and the question display
st.markdown("![Alt Text](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJqYW1tNzU1ZGozczhjdXNhODE1MWo4MG1uM3Rpd253enNzcjFndiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gLKVCVdLUXMTeIs6MD/giphy.webp)")

st.header("Quiz")

col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if col1.button("Prev"):
        prev_question()

with col3:
    if col3.button("Next"):
        next_question()

with col2:
    display_question()

download_button = st.sidebar.download_button(
    "Download Quiz Data",
    data=json.dumps(st.session_state.questions, indent=4),
    file_name="quiz_session.json",
    mime="application/json",
)
