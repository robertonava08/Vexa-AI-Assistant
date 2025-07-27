# Import the necessary libraries
import openai
from openai import OpenAI
import pyaudio
from faster_whisper import WhisperModel
import google.cloud.texttospeech as tts
import os
from dotenv import load_dotenv
import wave
import time
import simpleaudio as sa
import speech_recognition as sr
import pvporcupine
from pvrecorder import PvRecorder


# Loads the env file with the specific path 
env_path = "/home/robertonava08/Desktop/Vexa-AI-Assistant/.env" # needs specific path to work
load_dotenv(dotenv_path=env_path)

# Set the audio configurations using pyaudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 8
WAVE_OUTPUT_FILENAME = "voice.wav"

# Initialize pyaudio
p = pyaudio.PyAudio()

# Load the speech-to-text whisper model
model_size = "base" # used base as it is more accurate than tiny but can still run properly on the Pi
model = WhisperModel(model_size, device="cpu", compute_type="int8") # Run on CPU and uses int8 to reduce memory and increase speed 

# Call OpenAI api key and start client instance
api_key = os.getenv("OPENAI_API_KEY") 
client = OpenAI(api_key=api_key)

# Google credentials and initialize TTS client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vexa-ai-assistant-8bcdb8ccc1e1.json'
tts_client = tts.TextToSpeechClient()

# Get access key and path to ppn file for wake word
access_key = os.getenv("ACCESS_KEY")
wake_word_path = "/home/robertonava08/Desktop/Vexa-AI-Assistant/Hey-Vex_en_raspberry-pi_v3_0_0.ppn"

# Initialize porcupine
porcupine = pvporcupine.create(        
  access_key=access_key,        
  keyword_paths=[wake_word_path])

recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
recoder.start() # begins capturing audio into Picovoice engine

convo_history =  [
    {"role": "system", "content": "You are Vexa, a helpful, professional, sweet, and well spoken assistant,  you remember things the user has said previously in the conversation. "
    " Answer the user's questions directly if your name is slightly mispronounced, ignore it. When you are responding to the user ignore reading back things like :, *, symbols."}
]


while True:
   
   # Continously listen for wake word until it is heard
   pcm = recoder.read()
   result = porcupine.process(pcm)

   # Only if wake word is detected does logic for AI Assistant turn on 
   if result >= 0:
      print("Wake word detected")
      recoder.stop()

      try:
         while True:
            
            # Reanitialize pyaudio everytime the loop begins
            p = pyaudio.PyAudio()
            
            stream = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)


                  
            frames = []

            silence_recognizer = sr.Recognizer()

            silence_recognizer.pause_threshold = 1.75  # Wait up to 1.75 seconds of silence before Vexa begins responding 

            with sr.Microphone(sample_rate=RATE) as source:
               print("Vexa is listening")
               audio = silence_recognizer.listen(source, phrase_time_limit=None)
               print("Vexa is done listening")

            # Save the audio to file
            with open(WAVE_OUTPUT_FILENAME, "wb") as f:
               f.write(audio.get_wav_data())
            
         
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


            print("Detected language '%s' with probability %.2f%%" % (info.language, info.language_probability * 100)) # checks if correct language detected


            for segment in segments:
               print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

            # Combine all transcribed text into one string
            spoken_input = " ".join([segment.text for segment in segments])

            print(f"Transcribed input: {spoken_input}")

            # If user does not speak Vexa does not interact
            if not spoken_input.strip() or len(spoken_input.strip()) < 3:
               print("User is not active")
               recoder.start()
               continue  # Skip to next wake word

            convo_history.append({"role": "user", "content": spoken_input})


            completion = client.chat.completions.create(
                  model="gpt-3.5-turbo",
                  messages=convo_history
               )


            # Extract Vexa's response
            assistant_response = completion.choices[0].message.content


            # Print it out
            print(f"Vexa: {assistant_response}")


            convo_history.append({"role": "assistant", "content": assistant_response})



            MAX_MESSAGES = 25
            convo_history = [convo_history[0]] + convo_history[-MAX_MESSAGES:]


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
            response = tts_client.synthesize_speech(
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

            recoder.start()

      except KeyboardInterrupt:
         print("\nVexa is Shutting Down.")
