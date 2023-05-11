

import openai
import requests
import pylance 
import simpleaudio as sa
from pydub import AudioSegment

# Replace with your OpenAI and Eleven Labs API keys
openai_api_key = "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"
eleven_labs_api_key = "3ea525bd0795cc4367ca2016f0327d96"

openai.api_key = openai_api_key

def text_to_speech(text, api_key, voice_id, output_file="output.mp3"):
    url = "https://api.elevenlabs.com/synthesize"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "text": text,
        "voice": voice_id,
        "format": "mp3",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(response.content)

def play_audio(file):
    audio = AudioSegment.from_mp3(file)
    playback = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    playback.wait_done()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ],
    max_tokens=150,
    temperature=0.7,
)

text_response = response.choices[0].message['content']
print("Text response:", text_response)

voice_id = "2ugZx6PBjFO6Zq6IuNwe"  # Liv's voice ID
text_to_speech(text_response, eleven_labs_api_key, voice_id, "response.mp3")
print("Audio response saved as 'response.mp3'")

play_audio("response.mp3")