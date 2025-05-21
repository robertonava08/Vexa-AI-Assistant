# Import the necessary libraries

import openai 
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

model_size = "small"

# Run on CPU with INT8 (smaller memory usage, faster)
model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(
    "voice.wav",
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))