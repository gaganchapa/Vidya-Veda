from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
# from langchain_openai import ChatOpenAI
from langchain_ai21 import ChatAI21
TAVILY_API_KEY = "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"
# Define a set of instructions for the AI agent
instructions = """
As an experienced researcher, your expertise lies in finding high-quality and relevant information from the vast expanse of the Internet. Your task is to curate a selection of top-tier valid web links that provide valuable insights and in-depth knowledge on the given topic. Your goal is to ensure that the provided website links are vaid , authoritative, informative, and beneficial for users seeking to deepen their understanding of the subject matter. Be sure to include direct valid web links in your response. 
Be sure to include https webiste direct valid book links in your response. 
"""

import os
from getpass import getpass
# st.image("link.jpg")
st.markdown("![Alt Text](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjBqYzZwZG9zcmY5dDhubXF3YnozYm1nZ2R3NzVlYWp6M3d3Y2E3eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fb8maSaKTj3WVy2gFQ/giphy.webp)")

st.markdown("<h1 style='text-align: center; color: blue;'>LinkSage  </h1>", unsafe_allow_html=True)
st.markdown("Empower your study journey with our bot! We're here to help students easily discover valuable resources for their study topics, eliminating the hassle of searching for useful materials.")
st.divider()

f = open("user_data.txt", "r")
main = f.readline()
sub = f.readline()
q = main+"  "+ sub
os.environ["AI21_API_KEY"] = "lLYViWulXPnnL8i3i6UnhePluelfH9S1"
# Retrieve a template for creating AI functions from the hub
base_prompt = hub.pull("langchain-ai/openai-functions-template")

# Customize the base prompt with the specific instructions
prompt = base_prompt.partial(instructions=instructions)
# Initialize the ChatOpenAI with the GPT-4 model and a temperature setting of 0 for deterministic responses
# llm = ChatGoogleGenerativeAI(model="gemini",google_api_key="AIzaSyD1jyOLJLwsa2k1uLB3w4ckjdz1E_ImLRc")
# llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key="AIzaSyCL6FO4-SV6ApiDe-C5DGeca1tO0nms-Q0")
# --------------------------------------
llm = ChatAI21(model="j2-ultra",max_tokens=2048)
# ------------------------------------------
# from langchain_community.chat_models import ChatOllama
# llm = ChatOllama(model='llama2')

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from langchain_community.llms import HuggingFaceTextGenInference


# model = Llama2Chat(llm=llm)

# Initialize a custom search tool named TavilySearchResults
api_wrapper = TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY)
tavily_tool = TavilySearchResults(api_wrapper=api_wrapper)

# Aggregate the tools into a list for easy access
tools = [tavily_tool]

# Create an AI agent with the specified LLM and tools, and the customized prompt
agent = create_openai_functions_agent(llm, 
                                      tools, 
                                      prompt)

# Set up an executor for the agent, specifying the agent, tools, and enabling verbose output
agent_executor = AgentExecutor(agent=agent, 
                               tools=tools, 
                               verbose=True)
import datetime

# Get the current date and time
current_date = datetime.datetime.now()

# Format the current date as a string in 'YYYY-MM-DD' format
formatted_date = current_date.strftime('%Y-%m-%d')
# q = st.text_input("")
# Create a query string that includes the formatted date.
# query = f"""
# You are a course planner tasked with curating a rich collection of resources for users to explore and deepen their understanding of the given topic. Your objective is to provide a diverse range of materials, including blog posts and web-related links/websites, each accompanied by its respective website link. Additionally, conclude the list with a selection of recommended books related to the topic. Ensure the explanation is comprehensive, informative, and approximately 3 pages long. Remember to include direct web links for all provided resources.

# User's input - {q}
# """

query = f"""
Curate a diverse collection of resources for users to explore and deepen their understanding of the given topic. Provide a range of materials, including blog posts, web links, and GitHub repositories, each accompanied by its respective link. Conclude the list with a selection of recommended books related to the topic, including their titles and authors. The response should include only the links and titles without any introduction or conclusion.
User's input - {q}
"""
# query = f"""
# Curate a diverse collection of resources for users to explore and deepen their understanding of the given topic. Provide a range of materials, including blog posts, web links, and GitHub repositories, each accompanied by its respective link. Conclude the list with a selection of recommended books related to the topic, including their titles and authors. Ensure that all provided resources include the relevant links. The response must include only the links and titles without any introduction or conclusion.

# User's input - {q}
# """




result = agent_executor.invoke({"input": query})
st.write(result["output"])

