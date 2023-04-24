# Intro
This application is designed to allow users to interact with ChatGPT using speech-to-text (STT) and text-to-speech (TTS) technologies. Users can speak to the application and ChatGPT will respond using TTS.

Additionally, the assistant can improve itself by asking the user to write extensions. Extensions are code snippets that can be executed by the application to perform specific tasks, such as getting a list of files from a directory or opening a website in a browser. The user can write extensions and submit them to the assistant for it to learn and expand its capabilities.

The application combines natural language processing (NLP) with audio processing to create a more intuitive and interactive experience for the user. By integrating STT and TTS, the application enables users to communicate with ChatGPT using natural language, without the need for typing or reading. This can be particularly useful for users who have difficulty with typing or reading, or who simply prefer a more conversational style of interaction.

# Requirements

## Pydub Installation

Pydub requires ffmpeg to be installed on your system to work properly. Pydub uses ffmpeg to handle audio file format conversions and audio stream decoding. 

To install ffmpeg, follow these steps:

1. Go to the official ffmpeg website: https://ffmpeg.org/
2. Download the appropriate version for your system.
3. Add ffmpeg to your system's PATH environment variable so that Pydub can locate it.

## OpenAI Key setup

make sure to set the API key as environemtn variables
setx OPENAI_API_KEY "<YOUR_API_KEY>"

so that cn be retrieved like this
openai.api_key = os.environ.get("OPENAI_API_KEY")

## Log Viewer
I advice to use the log viewer extension in VS code.
Example of settings needed:
{
    "logViewer.watch": [
        {
            "pattern": "**/va_logs.log",
            "language": "log"
        }
    ],
    "logViewer.options": {
        
    }
}

make sure to go under the workspace settings
ctrl+shift+p

select extension
select log viewer
edit settings and add the json file that points to the logs

# config

## config.ini
This section specifies general settings for the application.

useLocalTTS = False
This setting determines whether the application will use a local TTS (Text-to-Speech) engine or Google TTS. If set to True, the application will use the local TTS engine installed on the system. If set to False, the application will use Google TTS to generate speech from text.

useLocalSTT = False
This setting determines whether the application will use a local STT (Speech-to-Text) engine or the OpenAI Whisper API. If set to True, the application will use the local STT engine installed on the system. If set to False, the application will use the OpenAI Whisper API to transcribe speech to text.

By default, both useLocalTTS and useLocalSTT are set to False, meaning that the application will use Google TTS and the OpenAI Whisper API for TTS and STT, respectively.

It's important to note that in order to use a local TTS or STT engine, it must be installed on the system and properly configured in the application.

# Google TTS
make sure to login to google in order to use google TTS or disable it from the config

# Formatter
use black formatter: https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0

