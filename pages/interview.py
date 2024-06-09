import speech_recognition as sr
import streamlit as st



import io
from streamlit_lottie import st_lottie

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import PromptTemplate

# llm = ChatOpenAI(api_key="AIzaSyBdEYoKwmQr3rTkB_rD77D_QBYxfDjPJwQ",
#                  model="google/gemma-2b-it",temperature=0.05)
from langchain_google_vertexai import VertexAI
from streamlit_lottie import st_lottie
import vertexai
# vertexai.init(project="saraswati-ai", location="us-central1")
from langchain_google_genai import ChatGoogleGenerativeAI
# llm = 
llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key="AIzaSyCL6FO4-SV6ApiDe-C5DGeca1tO0nms-Q0")
# Function to convert speech to text
if 'cht' not in st.session_state:
    st.session_state['cht'] = []
def speech_to_text(ser):
    recognizer = sr.Recognizer()  
    template1 = """ See this is the text from user . This is the user's course or branch {topic} based on this generate the solution . Based on the topic ask Technical questions . 
        You are a  reviewer and gives feedback to his answers . check the user's text or words. check the words , sentence and unnecessary things. 
        This text is generated from speech to text so main goal here is check oral test i mean english speaking skills so go through text check errors , 
        sentence construction mistakes , every wrong and mistakes in it and give a summary what to do and how to improve it 
        previous chat history -  user text - {text1}
        {chat_history}
        So see the chat history and don't repeat the questions . for each question give feedback. Only give one question for now when y see chat history updated you can understand i am running in loop so when i call give on question only
        
        """
    template2 = """ You are a helpful AI assistant . you are also called the interviewer total questions you ask are 1.Only ask one Technical question 
    User gives you what branch he is in {topic} then based on that you will ask questions. 
    First ask hr questions like strength , weaknesses , how you handle failures etc .. like that generate more and different types but ask only three questions from it 
    Next another 3 questions ask based on subject or topic he gave .Only give one question for now when y see chat history updated you can understand i am running in loop so when i call give on question only
        Only ask one question 
    previous chat history - 
    {chat_history}
    So see the chat history and don't repeat the questions .
    
    """
    
    prompt = PromptTemplate(
        template=template1, input_variables=['topic','chat_history','text1']
    )
    chain = prompt | llm
    prompt1 = PromptTemplate(
            template=template2, input_variables=['topic','chat_history']
        )
    chain1 = prompt1 | llm
    with sr.Microphone() as source:
        res1 = chain1.invoke({'topic':ser,'chat_history':st.session_state['cht']})
        st.write("Question:",res1)
        print("Listening...")
        st.write("Listening...")
        
        recognizer.adjust_for_ambient_noise(source)
        
        # Record audio for 10 seconds or until speech is detected
        audio = recognizer.listen(source, timeout=40)
        
        print("Processing...")
        st.write("Processing...")
        

    try:
        # Use Google Speech Recognition to convert speech to text
        text = recognizer.recognize_google(audio)
        # print("You said:", text)
        st.write("You said:", text)
        
        
        res = chain.invoke({'topic':ser,'chat_history':st.session_state['cht'],'text1':text})
        st.write("feedback:",res)
        
        
        
        st.session_state['cht'].append([{'topic': ser,'question':res1,'user':text,'chatbot':res}])
        
        # st.write("Chatbot - ",res)
        # Save audio to an MP3 file
        # audio_segment = AudioSegment.from_file(io.BytesIO(audio.frame_data), format="wav")
        # audio_segment.export("output.wav", format="wav")
        # audio.export("output.mp3", format="mp3")
        # print("Audio saved as output.mp3")
        # st.write("Audio saved as output.mp3")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        st.write("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Sorry, an error occurred: {e}")
        st.write(f"Sorry, an error occurred: {e}")

# Streamlit app
def main():
    st.title("Interview Assistant")
    import requests
    url_json = dict()
    url = requests.get("https://lottie.host/1be7691d-8e6d-4526-86a1-1aec07cecf20/3W63jiF4yP.json")
    url_json = url.json()
    with st.sidebar:
        st_lottie(url_json,reverse=True, 
        # height and width of animation 
        height=300,   
        width=300, 
        # speed of animation 
        speed=1,   
        # means the animation will run forever like a gif, and not as a still image 
        loop=True,   
        # quality of elements used in the animation, other values are "low" and "medium" 
        quality='high', 
        # THis is just to uniquely identify the animation 
        key='Car' )
        
        
        
        
    st.write("""The app begins with prompting the user to input the topic or branch for the interview questions they wish to receive. Upon providing the input, the user initiates the speech recording process by clicking the "Start Recording" button. The app then listens for speech input, providing feedback in real-time. If there is a silence lasting longer than 10 seconds, the recording stops automatically, and the app proceeds to analyze the provided speech, offering feedback based on the input received.
""")
    ser =  st.text_input("Topic:", placeholder="Your Query", key='input1222')

    # Button to start speech recognition
    count = 0
 
    if ser and st.button("Start Interview"):
        speech_to_text(ser)
        
        # st.session_state['count'] +=1
        # if st.button('next') and st.session_state['count']<6:
        # speech_to_text(ser)
            

# Run the app
if __name__ == "__main__":
    main()

