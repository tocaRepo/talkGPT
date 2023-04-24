import wave
import time
from pydub import AudioSegment
import numpy as np
from pydub.playback import play
import utils.VAConstants as constants
import datetime
import openai
from utils.logger import Logger

# Create a logger instance with the name "audioService"
logger = Logger("audioService")


def detect_noise(data, threshold):
    audio_data = np.frombuffer(data, dtype=np.int16)
    peak_value = np.max(np.abs(audio_data))
    # logger.info('[detect_noise] - Peak value: '+str(peak_value) )
    if peak_value > threshold:
        logger.info("[detect_noise] - detected noise - Peak value: " + str(peak_value))
        return True
    return False


def record_audio_V2(stream, pyAudio, isStopped):
    """
    Records audio from the microphone and saves it to a WAV file.
    """

    data = stream.read(constants.CHUNK)
    if detect_noise(data, constants.HEADPHONE_THRESHOLD):
        logger.info("[" + __name__ + "] - noise detected")
        frames = []
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Construct the filename with the timestamp
        filename = constants.OUTPUT_FOLDER + constants.WAVE_OUTPUT_FILENAME + ".wav"

        for i in range(
            0, int(constants.RATE / constants.CHUNK * constants.RECORD_SECONDS)
        ):
            if isStopped > 0:
                # Stop recording
                stream.stop_stream()  # stop the audio input stream
                pyAudio.terminate()  # terminate the PyAudio object
            else:
                data = stream.read(constants.CHUNK)
                # if(detect_noise(data,constants.SOFT_THRESHOLD)):
                frames.append(data)

        if isStopped == 0:
            # Write the audio file
            with wave.open(filename, "wb") as wf:
                wf.setnchannels(constants.CHANNELS)
                wf.setsampwidth(pyAudio.get_sample_size(constants.FORMAT))
                wf.setframerate(constants.RATE)
                wf.writeframes(b"".join(frames))

            audio = AudioSegment.from_wav(
                constants.OUTPUT_FOLDER + constants.WAVE_OUTPUT_FILENAME + ".wav"
            )
            mpName = constants.OUTPUT_FOLDER + "audio_" + timestamp + ".mp3"
            audio.export(mpName, format="mp3")
            return mpName
        return ""


def record_audio(stream, pyAudio):
    """
    Records audio from the microphone and saves it to a WAV file.
    """
    frames = []
    for i in range(0, int(constants.RATE / constants.CHUNK * constants.RECORD_SECONDS)):
        data = stream.read(constants.CHUNK)
        frames.append(data)
    # Write the audio file
    with wave.open(
        constants.OUTPUT_FOLDER + constants.WAVE_OUTPUT_FILENAME, "wb"
    ) as wf:
        wf.setnchannels(constants.CHANNELS)
        wf.setsampwidth(pyAudio.get_sample_size(constants.FORMAT))
        wf.setframerate(constants.RATE)
        wf.writeframes(b"".join(frames))


def transcribe_audio(mpName, model):
    """
    Transcribes audio from an MP3 file using the Whisper speech recognition pipeline.
    """
    start_time = time.time()
    result = model.transcribe(mpName)
    logger.info("[" + __name__ + "] - detected: " + result["text"])
    end_time = time.time()
    execution_time_ms = int((end_time - start_time) * 1000)
    logger.info(
        "["
        + __name__
        + "] - transcribe_audio Execution time: %d ms" % execution_time_ms
    )
    return result["text"]


def transcribe_audio_whisper_api(audio_file):
    """
    Generates a response to a given prompt using the OpenAI GPT-3 API.
    """
    logger.info("[" + __name__ + "] - transcribe" + audio_file)
    audio_file = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en")
    logger.info("[" + __name__ + "] - transcript:" + transcript.text)
    return transcript.text
