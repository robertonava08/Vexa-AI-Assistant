# Import the necessary libraries
import openai
from openai import OpenAI
import pyaudio
import pygame
from faster_whisper import WhisperModel
import google.cloud.texttospeech as tts
import numpy as np
import os
from dotenv import load_dotenv
import wave
import time
import simpleaudio as sa


# Try loading .env explicitly with full path
env_path = "/home/robertonava08/Desktop/Vexa-AI-Assistant/.env"#load what is stored in my .env file

load_dotenv(dotenv_path=env_path)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 8
WAVE_OUTPUT_FILENAME = "voice.wav"


p = pyaudio.PyAudio()


stream = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)


print("* recording")


frames = []


for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
   data = stream.read(CHUNK)
   frames.append(data)


print("* done recording")


stream.stop_stream()
stream.close()
p.terminate()


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()




wave_obj = sa.WaveObject.from_wave_file("voice.wav")
play_obj = wave_obj.play()
play_obj.wait_done()  # wait until playback finishes


model_size = "base"# model is being loaded from faster-whisper library


# Run on CPU with INT8 (smaller memory usage, faster)
model = WhisperModel(model_size, device="cpu", compute_type="int8")


segments, info = model.transcribe(
   "voice.wav",
   beam_size=5,
   vad_filter=True,
   vad_parameters=dict(min_silence_duration_ms=500),
)


# Convert 'segments' generator to a list so we can access all transcribed parts multiple times.
# Generators yield items one by one and can't be reused or printed directly,
# but a list holds all items at once, making it easier to work with.


segments = list(segments)  # <-- This is important!


print("Detected language '%s' with probability %.2f%%" % (info.language, info.language_probability * 100))


for segment in segments:
   print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))



api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

# Combine all transcribed text into one string
spoken_input = " ".join([segment.text for segment in segments])




print(f"Transcribed input: {spoken_input}")


# Message section is what you are telling Vexa
message =  {"role": "user", "content": spoken_input}


conversation = [
   {"role": "system", "content": "You are Vexa a helpful, quirky, sweet, super energetic but somewhat edgy assistant assistant. Answer the users questions directly and playfully."},
    {
     "role" : "user",
     "content" : spoken_input
    }
   ]
completion = client.chat.completions.create(
   model="gpt-3.5-turbo",
   messages=conversation
)


# Extract Vexa's response
assistant_response = completion.choices[0].message.content


# Print it out
print(f"Vexa: {assistant_response}")

# Begin text-to-speech code (trial code)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vexa-ai-assistant-8bcdb8ccc1e1.json'

client = tts.TextToSpeechClient()

# This sets the text input that we want to be synthesized 
synthesis_input = tts.SynthesisInput(text=assistant_response)

# We choose what voice we want to use here 
voice = tts.VoiceSelectionParams(
   language_code="en-AU",
   name="en-AU-Chirp3-HD-Leda"
 )

# Select the type of audio file you want returned
audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.LINEAR16  # Compatible with simpleaudio
)

# Perform the text-to-speech request
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save the audio to a .wav file
with open("vexa_response.wav", "wb") as out:
    out.write(response.audio_content)

# Play the generated audio
wave_obj = sa.WaveObject.from_wave_file("vexa_response.wav")
play_obj = wave_obj.play()
play_obj.wait_done()