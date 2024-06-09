import streamlit as st
from streamlit_player import st_player
import json

# ==================
from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS #facebook AI similarity search
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
# ==================
st.markdown("![Alt Text](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmJ4enF3ZXE3dWFnend0YnJpdWgyeGp2MHp3YTZqcnBneDR5ZGpibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5k5vZwRFZR5aZeniqb/giphy.webp)")

st.title("VidyaVeda – Empowering Learning with Personalized AI")
# st.sidebar.markdown("![Alt Text](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm1zZnVkdjR4dXluY2Zqc21yd3pobWM0Mm5wdDc1ZmVjYmk4M2FybCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/CVtNe84hhYF9u/giphy.webp)")
st.sidebar.title("VidyaVeda – Empowering Learning with Personalized AI")
st.sidebar.subheader("This project proposes a app that uses Generative AI to personalize student learning by curating video lectures and generating concise notes from videos and PDFs. The app includes interactive quizzes tailored to specific concepts and provides performance analysis reports to highlight strengths and weaknesses. It empowers students with personalized learning, enhanced efficiency, deeper understanding, and self-directed education.")
st.sidebar.caption("powered by [**YouData.ai**](https://www.youdata.ai/auth/signin?redirect_to=/hackathon/0)", unsafe_allow_html=True)
st.sidebar.image("you.png")
text_input = st.text_input(
        "Enter Main Theme You want to study👇"
    )

text_input_2 = st.text_input("Enter the Sub Theme You want to Study👇")
load_dotenv()

with open('user_data.txt', 'w') as f:
    # for line in lines:
    f.write(text_input)
    f.write('\n')
    f.write(text_input_2)
# st.set_page_config(page_title="Ask your PDF")
# st.header("Ask Your PDF")
# pdf = st.file_uploader("Upload your pdf",type="pdf")
# with st.spinner('Wait for it...'):
#     if pdf is not None:
#         pdf_reader = PdfReader(pdf)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()

#         # spilit ito chuncks
#         text_splitter = CharacterTextSplitter(
#             separator="\n",
#             chunk_size=1000,
#             chunk_overlap=200,
#             length_function=len
#         )
#         chunks = text_splitter.split_text(text)

#         # create embedding
#         embeddings = HuggingFaceEmbeddings()

#         knowledge_base = FAISS.from_texts(chunks,embeddings)


from simplet5 import SimpleT5
import os
from googleapiclient.discovery import build
from pytube import YouTube


def download_youtube_video(url, output_path='videoplayback.mp4'):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        stream.download(filename=output_path)
        
        print(f"Video '{yt.title}' has been downloaded successfully as {output_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def youtube_search(query):
    # Replace with your own API key
    api_key = 'AIzaSyByyiNnGHhxY2PYDIB5X8SaGAmX9lEGAMY'
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Perform a search query
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1,
        type='video'
    )
    response = request.execute()

    # Extract the video link
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        return video_title, video_link
    else:
        return None, None

# if __name__ == '__main__':
#     query = input("Enter the search query: ")
#     title, link = youtube_search(query)
#     if link:
#         print(f'Video Title: {title}\nVideo Link: {link}')
#     else:
#         print('No results found.')
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import re
if text_input_2:
    # url = 'https://youtu.be/f-UPh5-IuOE?si=3KkTquMpRo80gRxQ'
    inp = text_input+text_input_2
    title, link = youtube_search(inp)
    url = link
    download_youtube_video(url)
    subprocess.run(['python', "trans.py"], check=True, capture_output=True, text=True)
    file_highlights = 'highlights.json'
    file_chapters = 'chapters.json'

    placeholder = st.empty()
    with placeholder.container():
        st_player(url, playing=False, muted=True)
        
    # mode = st.sidebar.selectbox("Summary Mode", ("Highlights", "Chapters"))

    def get_btn_text(start_ms):
        seconds = int((start_ms / 1000) % 60)
        minutes = int((start_ms / (1000 * 60)) % 60)
        hours = int((start_ms / (1000 * 60 * 60)) % 24)
        btn_txt = ''
        if hours > 0:
            btn_txt += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        else:
            btn_txt += f'{minutes:02d}:{seconds:02d}'
        return btn_txt


    def add_btn(start_ms, key):
        start_s = start_ms / 1000
        if st.button(get_btn_text(start_ms), key):
            url_time = url + '&t=' + str(start_s) + 's'
            with placeholder.container():
                st_player(url_time, playing=True, muted=False)
            
    st.subheader("Overview of the Video")
    model = SimpleT5()
# Extract the string after "?v=" using a regular expression
    match = re.search(r"\?v=(.*)", url)
    extracted_string = match.group(1)
    srt = YouTubeTranscriptApi.get_transcript(extracted_string)
    srt_mine = ""
    for i in srt:
        # file.write(i['text'])
        srt_mine += i['text'] + " "
    # st.write("Transcript of the video")
    model.load_model("t5","D:\VedaVidya\simplet5-epoch-4-train-loss-1.2292-val-loss-1.6766", use_gpu=False)
    # text_to_summarize = 
    summ = model.predict(srt_mine)
    st.write(summ)
    # st.caption(f"Powered by [**{"YouData.ai"}**](https://www.youdata.ai/auth/signin?redirect_to=/hackathon/0)", unsafe_allow_html=True)
    # st.caption(f"[**{Link to the Dataset}**](https://www.kaggle.com/datasets/gagandwaz/summary)", unsafe_allow_html=True)



    # if mode == "Highlights":
    st.subheader("Highlights")
    with open(file_highlights, 'r') as f:
        data = json.load(f)
    results = data['results']

    cols = st.columns(3)
    n_buttons = 0
    for res_idx, res in enumerate(results):
        text = res['text']
        timestamps = res['timestamps']
        col_idx = res_idx % 3
        with cols[col_idx]:

            st.write(text.capitalize())
            for t in timestamps:
                start_ms = t['start']
                add_btn(start_ms, n_buttons)
                n_buttons += 1
                break
    st.subheader("Summary")
    with open(file_chapters, 'r') as f:
            
            chapters = json.load(f)

    for chapter in chapters:
        start_ms = chapter['start']
        add_btn(start_ms, None)
        txt = chapter['summary']
        st.write(txt)

# if st.button("Generate the AI Video Notes"):
#     pass

#     # st.button("Reset", type="primary")
# if st.button("Ask Questions Based on Pdf"):
#     user_question = st.text_input("Ask Question about your PDF:")
#     if user_question:
#             docs = knowledge_base.similarity_search(user_question)
#             llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":5,"max_length":64},huggingfacehub_api_token="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")
#             chain = load_qa_chain(llm,chain_type="stuff")
#             response = chain.run(input_documents=docs,question=user_question)

#             st.write(response)


        
    # st.write("Why hello there")


# else:
    # with open(file_chapters, 'r') as f:
    #     chapters = json.load(f)
    # for chapter in chapters:
    #     start_ms = chapter['start']
    #     add_btn(start_ms, None)
    #     txt = chapter['summary']
    #     st.write(txt)

