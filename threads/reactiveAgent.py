import time
from service.textToSpeechService import textToSpeechService
import service.chatGPTService as chatgptService
import random
from database.memory import Memory

from utils.logger import Logger

import utils.contextHolder as context
from utils.parser import Parser
import json



# Create a logger instance with the name "reactiveAgent"
logger = Logger("reactiveAgent")
tts = textToSpeechService()


def get_queue_message(interpeterQueue, concatenated_text):
    # Loop through the queue until it's empty
    while not interpeterQueue.empty():
        # Get the next string from the queue
        text = interpeterQueue.get()
        # Concatenate the string to the previously concatenated text
        concatenated_text += text
    return concatenated_text


def listen_queue_for_multiple_messages(interpeterQueue):
    concatenated_text = ""
    politenessCounter = 0  # allow an extra 10
    beingRude = False
    while (not interpeterQueue.empty() or politenessCounter < 3) and (
        beingRude is False
    ):
        concatenated_text = get_queue_message(interpeterQueue, concatenated_text)
        time.sleep(1)  # wait some time in case the speaker it's still talking
        politenessCounter = politenessCounter + 1
        if politenessCounter > 10:
            beingRude = True
            logger.warning("AI stop being polite and jump in the conversation")
    return concatenated_text


def job(interpeterQueue, stop_recording, memory):
    # Initialize an empty string to store the concatenated text
    transcription = listen_queue_for_multiple_messages(interpeterQueue)
    logger.info("[reactiveAgent] - listening for messages")
    if transcription:
        stop_recording.set()
        logger.info("[reactiveAgent] - send stop recording signal")
        logger.info("[reactiveAgent] - messages found:" + transcription)
        
        response = chatgptService.generate_response(transcription,memory.query_index(transcription), context.previousUserPrompt,context.previousSystemResponse)
        context.previousUserPrompt=transcription
        context.previousSystemResponse=response
        logger.info("[reactiveAgent] - processing response:" + response)
        if response:
            tts.text_to_speech(response)
            
        time.sleep(random.randint(1, 3))
        # Some time later, when you want to start recording again:
        logger.info("[reactiveAgent] - asks to resume recording")
        stop_recording.clear()  # clear the event to allow recording to continue

        memory.add_elements_to_index(
            "user:" + transcription + ", system:" + response, "interaction"
        )

    # Wait for 0.5 seconds before running the job again
    time.sleep(random.randint(3, 5))


def run_job(interpeterQueue, stop_recording):
    # Run the job continuously
    memory = Memory()

    while True:
        job(interpeterQueue, stop_recording, memory)
