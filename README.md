# Vexa-AI-Assistant
AI voice assistant designed to interact with users in a natural and intuitive way and assist them in their daily tasks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)\
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Screenshots](screenshots)
- [Documentation Used](#documentation-used)
- [Development Log](#development-log)


### Installation




### Usage



### Features



### Contributing



### License



### Screenshots


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
