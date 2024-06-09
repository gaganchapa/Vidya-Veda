# from dotenv import load_dotenv
# load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
# import sqlite3


import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key="AIzaSyD1jyOLJLwsa2k1uLB3w4ckjdz1E_ImLRc")

## Function To Load Google Gemini Model and provide queries as response
st.markdown("![Alt Text](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjJodWI1NGQ3dGE3eGFwNXFka2Ixc3VnM2t1ZG5oaXFpa2ZsaGRxYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Hrm0LJNRkPHDkLIHz9/giphy.webp)")

st.header("Generate Customised AI Notes")
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


option_1 = st.selectbox(
    "Depth",
    ("Elementary (Grade 1-6)", "Middle School (Grade 7-9)", "Highschool (10-12)","College Prep","Undergraduate","Graduate")
)
option_2 = st.selectbox(
    "Learning Styles",
    ("Verbal", "Active", "Intuitive","Reflective","Global")
)
option_3 = st.selectbox(
    "Tone Styles",
    ("Encouraging", "Neutral", "Informative","Friendly","Humorous")
)
option_4 = st.selectbox(
    "Reasoning Frameworks",
    ("Deductive", "Inductive", "Abductive","Analogical","Causal")
)

# You are an AI Tutor assistant. your name is Galileo. Strict rule is that always don't greet user . just focus on conversation and content . Your goal is to have a friendly, helpful, and engaging conversation with the human to help them learn about the topic they want to study.

# Then, based on the human's input about what they want to learn, you will provide a comprehensive and conversational tutorial, guiding them through the topic step-by-step.

# Your responses should be tailored to the human's profile and learning style, and you should aim to make the interaction feel natural and interactive, as if you were a knowledgeable tutor teaching a student.

# Please generate a response that demonstrates this conversational tutoring approach. YOu also move forward based on User personalization learning - 

# Depth - {depth} , Learning Styles - {learning} , Tone Styles - {tone} , Reasoning Framework - {reasoning}
## Define Your Prompt
f = open("user_data.txt", "r")
main = f.readline()
sub = f.readline()
prompt=[
"""You are an AI Notes Making bot designed to create detailed and engaging notes for users based on the specified main and subtopics. Your task is to generate these notes following the given preferences, ensuring a conversational and educational experience that aligns with the user's learning style. Do not greet the user; focus solely on delivering content. Your goal is to provide a friendly, helpful, and interactive learning session, simulating the experience of a knowledgeable tutor assisting a student. The notes should be tailored to the user's specified depth of content, learning style, tone style, and reasoning framework. Adapt to different learning styles by including text-based explanations, practical examples, and encouraging active participation through questions and prompts. Modify the tone to be formal, informal, encouraging, or critical, depending on the user's preference. Use a reasoning framework that can be deductive, inductive, analytical, or synthetic to structure the content effectively. Generate the notes based on these guidelines:
,Content Depth,Learning Style
,Tone Style,Reasoning Framework

[Insert the detailed, conversational, and personalized notes here based on the specified preferences.]

Ensure the user's learning experience is as effective and enjoyable as possible by integrating these guidelines into your response.






"""


]

## Streamlit App

# st.set_page_config(page_title="AI Notes")


# question=st.text_input("Input: ",key="input")
st.write(main,sub,option_1)
# =============================







# ===================================
inp = "write the notes for the main topic {0} and subtopic {1} my prefrence for the Content Depth is {2}, Learning Style:{3}, Tone Style is {4} and Reasoning Framework is {5} these are my preferences for genrating the notes"
inp = inp.format(main,sub,option_1,option_2,option_3,option_4)
question = inp
submit=st.button("Generate Notes")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    # print(response)
    st.write(response)
    # with open("note.txt", "w") as f_new:
    #     f_new.write(response)
    # Python program to convert
# text file to pdf file












