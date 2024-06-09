import requests
import pprint
import json
import time
from api_secrets import API_KEY_ASSEMBLYAI


upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers_auth_only = {'authorization': API_KEY_ASSEMBLYAI}

headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}


CHUNK_SIZE = 5_242_880  # 5MB


def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                                    headers=headers_auth_only,
                                    data=read_file(filename))
    pprint.pprint(upload_response.json())
    return upload_response.json()['upload_url']


def transcribe(audio_url):
    transcript_request = {
        'audio_url': audio_url,
        'auto_chapters': True,
        'auto_highlights': True
    }

    transcript_response = requests.post(transcript_endpoint,
                                        json=transcript_request,
                                        headers=headers)
    pprint.pprint(transcript_response.json())
    return transcript_response.json()['id']


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)

    if polling_response.json()['status'] == 'completed':
        filename = transcript_id + '.txt'
        with open(filename, 'w') as f:
            f.write(polling_response.json()['text'])

        filename ='chapters.json'
        with open(filename, 'w') as f:
            chapters = polling_response.json()['chapters']
            json.dump(chapters, f, indent=4)
            
        filename = 'highlights.json'
        with open(filename, 'w') as f:
            data = polling_response.json()['auto_highlights_result']
            json.dump(data, f, indent=4)

        print('Transcript saved')
        return True
    return False


def pipeline(filename):
    audio_url = upload(filename)
    transcribe_id = transcribe(audio_url)
    while True:
        result = poll(transcribe_id)
        if result:
            break
        # print("waiting for 60 seconds")
        # time.sleep(60)


from pytube import YouTube

def download_youtube_video(url, output_path='.'):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        stream.download(output_path=output_path)
        
        print(f"Video '{yt.title}' has been downloaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# if __name__ == '__main__':
#     url = input("Enter the YouTube video URL: ")
#     output_path = input("Enter the output path (default is current directory): ") or '.'
#     download_youtube_video(url, output_path)

if __name__ == '__main__':

   
   pipeline('videoplayback.mp4')