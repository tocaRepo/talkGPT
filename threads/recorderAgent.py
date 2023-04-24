import time
import pyaudio
import utils.VAConstants as constants
import service.audioService as audioService
from utils.logger import Logger

# Create a logger instance with the name "recorderAgent"
logger = Logger("recorderAgent")


def job(recorderQueue, pyAudio, stream, isStopped):
    # The code that should be executed every 5 seconds

    filename = audioService.record_audio_V2(stream, pyAudio, isStopped)
    if filename:
        recorderQueue.put(filename)
        logger.info("[recorderAgent] - " + filename + " processed")
    # Wait for 0.5 seconds before running the job again
    time.sleep(0.5)


def run_job(recorderQueue, stop_recording):
    # Run the job continuously
    """Run the recorderAgent job."""
    # Restart recording
    pyAudio = pyaudio.PyAudio()  # create a new PyAudio object
    stream = pyAudio.open(
        format=constants.FORMAT,
        channels=constants.CHANNELS,
        rate=constants.RATE,
        input=True,
        frames_per_buffer=constants.CHUNK,
    )  # create a new audio input stream
    # Start recording
    stream.start_stream()
    isStopped = 0
    while True:
        # Check if the stop event has been set
        if stop_recording.is_set():
            if isStopped == 0:
                # Stop recording
                stream.stop_stream()  # stop the audio input stream
                pyAudio.terminate()  # terminate the PyAudio object
                logger.info("[recorderAgent] - stop recording")
                isStopped = 1
            # Wait for the event to be cleared before resuming recording
        else:
            isStopped = 0
            # Restart recording
            pyAudio = pyaudio.PyAudio()  # create a new PyAudio object
            stream = pyAudio.open(
                format=constants.FORMAT,
                channels=constants.CHANNELS,
                rate=constants.RATE,
                input=True,
                frames_per_buffer=constants.CHUNK,
            )  # create a new audio input stream
            # Start recording
            stream.start_stream()
            job(recorderQueue, pyAudio, stream, isStopped)
