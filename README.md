# Vexa-AI-Assistant
AI voice assistant designed to interact with users in a natural and intuitive way and assist them in their daily tasks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Screenshots](screenshots)
- [Documentation Used](#documentation-used)
- [Development Log](#development-log)


### Installation
* Install Visual Studio Code IDE 
* Install Python 3
    -- Verify with: python3 --version
* Install Python Extension for VS Code
* Create and activate a virtual environment (Linux)
  In your project directory:
    -- python3 -m venv venv 
    -- source venv/bin/activate
* Install required dependencies (libraries liested at the top of script)
* Create a .env file and insert your keys
  In project folder add: 
    -- OPENAI_API_KEY=your_openai_api_key
    -- ACESS_KEY=your_picovoice_access_key
* Press "run" button or run manually 


### Usage
* Run script 
* Speak the wake word "Hey Vexa." 
* Speak a question or command
* Command + C 2x to terminate Vexa

### Features
* Always-on Wake Word Detection
    - Continously listens for the wake word using a real-time audio stream with Picovoice Porcupine

* Natural Speech Recognition
    - Transcribes spoken input using Faster-Whisper for fast and accurate speech-to-text conversion

* Conversational Short-Term Memory
    - Remembers recent interactions using OpenAI's chat history to maintain natural conversation flow

* Lifelike Voice Output
    - Uses Google Cloud Text-to-Speech to respond with a realistic and pleasant voice

* Seamless Audio Pipeline 
    - Modular system for capturing audio, generating responses, and playing voice output in real time


### License
This project is licensed under the [MIT License](./LICENSE)
Feel free to use or modify the code -- just make sure to give credit. 


### Videos

Click link to watch a short demo video: https://youtube.com/shorts/uBmfoppIMZI 


### Documentation Used
* https://www.youtube.com/watch?v=GVPWz-nhJhg -- Very useful tutorial on how to use Googles text-to-speech API effectively
* https://www.dotenv.org/docs/ -- dotenv library was used to keep api keys for openai and pvporcupine secure (highly important)
* https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio-documentation -- pyaudio library used record audio and process the user stream
* https://pypi.org/project/simpleaudio/ -- simpleaudio library is what allows Vexa's voice to be heard by playing back the .wav file
* https://pypi.org/project/faster-whisper/ -- faster whisper library used for speech-to-text transcription 
* https://platform.openai.com/docs/overview -- openai api is the brain of the whole program because it allows for the AI Assistant to respond to user
* https://picovoice.ai/docs/ -- pvporcupine and pvrecoder used to create custom wake word and allow hardware to listen for wakeword


### Development Log
* 06/17/25
    -- The logic of the program is running smooth and everything is in order,
        the next step in development is to create an infinite loop so that the user
        does not need to rerun the program constantly.
* 07/11/25
    -- Solved the issue of the speaker and mic drawing too much current from the USB ports 
        on the Raspberry Pi by using a powered USB adapter.
    -- Program is now running smoothly, now what is needed is to add memory and a wake word like "Hey, Vexa."
* 07/24/25
    -- Using the libraries pvporcupine and pvrecorder I have successfully added the wake word "Hey, Vexa" to the program.
        Now when Vexa will only respond with the wake word when initially turned on and even after "shutting it down"
* 07/25/25
    -- Today's stage of development will involve adding short-term memory for a natural conversation flow and friendly user experience
* 07/26/25
    -- Updated Vexa so that she no longer only listens for 8 seconds but listens until user is done speaking (waits 1.75 of silence to respond).
       I have deleted the section that plays back the user audio to reduce the responce time of Vexa (it worked) 