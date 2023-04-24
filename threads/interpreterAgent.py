import time
import whisper
import service.audioService as audioService
import os
from utils.logger import Logger
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

use_local_stt = eval(config["General"]["useLocalSTT"])
# Create a logger instance with the name "interpreterAgent"
logger = Logger("interpreterAgent")


def is_english(string):
    """
    Check if a string only contains English characters (ASCII).

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string only contains English characters, False otherwise.
    """
    try:
        string.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return "no"
    else:
        return "yes"


def job(recorderQueue, interpeterQueue, name, model):
    mpFilename = recorderQueue.get()
    logger.info("[" + name + " interpreterAgent] - check the queue")
    if mpFilename:
        text = ""
        if use_local_stt:
            text = audioService.transcribe_audio(mpFilename, model)
        else:
            text = audioService.transcribe_audio_whisper_api(mpFilename)

        logger.info("speech to text performed on: " + mpFilename)
        if text and len(text) > 5:
            response = is_english(text)
            logger.info("input: " + text + " accepted?" + response)
            if "yes" in response.lower() or "sure" in response.lower():
                interpeterQueue.put(text)
                # Check if the file exists
                if os.path.isfile(mpFilename):
                    # If the file exists, delete it
                    os.remove(mpFilename)
                    logger.info(f"{mpFilename} has been deleted.")
                else:
                    # If the file doesn't exist, logger.info an error message
                    logger.info(f"{mpFilename} does not exist in the folder.")
                # Wait for 5 seconds before running the job again
            else:
                logger.info("nothing it has been detected on: " + mpFilename)

    time.sleep(1)


def run_job(recorderQueue, interpeterQueue, name):
    # Run the job continuously
    model = None
    if use_local_stt:
        # Set up the speech recognition pipeline
        # https://github.com/openai/whisper
        # model = whisper.load_model("base")
        # model = whisper.load_model("small")
        model = whisper.load_model("base")

    while True:
        logger.info("[" + name + " interpreterAgent] - it's been executed")
        job(recorderQueue, interpeterQueue, name, model)
