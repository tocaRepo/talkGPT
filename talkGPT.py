import threading
import openai
import threads.recorderAgent as recorderAgent
import threads.interpreterAgent as interpreterAgent
import threads.interpreterAgent as interpreterAgent
import threads.readerAgent as readerAgent
import threads.reactiveAgent as reactiveAgent
from service.textToSpeechService import textToSpeechService
import queue
import configparser
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

config = configparser.ConfigParser()
config.read("config.ini")

use_local_stt = eval(config["General"]["useLocalSTT"])
recorder_agent_enabled = eval(config["General"]["recorderAgentEnabled"])
interpreter_agent_enabled = eval(config["General"]["interpreterAgentEnabled"])
reactive_agent_enabled = eval(config["General"]["reactiveAgentEnabled"])
reader_agent_enabled = eval(config["General"]["readerAgentEnabled"])


tts = textToSpeechService()
# Set up the OpenAI API
openai.api_key = OPENAI_API_KEY

# Create a threading Event object to signal when to stop recording
stop_recording = threading.Event()
# Create a new queue to hold the filenames
recorderQueue = queue.Queue()
# Create a new queue to hold prompt
interpeterQueue = queue.Queue()

tts.utility_response("Let's have a chat!")

# Record audio in realtime
if recorder_agent_enabled:
    recorderThread = threading.Thread(
        target=recorderAgent.run_job,
        args=(
            recorderQueue,
            stop_recording,
        ),
    )
    recorderThread.start()

# read text in realtime
if reader_agent_enabled:
    readerThread = threading.Thread(target=readerAgent.run_job, args=(interpeterQueue,))
    readerThread.start()

# speech to text
if interpreter_agent_enabled:
    interpreterThread = threading.Thread(
        target=interpreterAgent.run_job, args=(recorderQueue, interpeterQueue, "john")
    )
    interpreterThread.start()
    if use_local_stt:
        # local TTS needs more thread to work realtime
        # speech to text
        interpreterThread = threading.Thread(
            target=interpreterAgent.run_job,
            args=(recorderQueue, interpeterQueue, "ned"),
        )
        interpreterThread.start()
        # speech to text
        interpreterThread = threading.Thread(
            target=interpreterAgent.run_job,
            args=(recorderQueue, interpeterQueue, "jim"),
        )
        interpreterThread.start()

# compute and speak
if reactive_agent_enabled:
    reactiveAgent = threading.Thread(
        target=reactiveAgent.run_job,
        args=(
            interpeterQueue,
            stop_recording,
        ),
    )
    reactiveAgent.start()

