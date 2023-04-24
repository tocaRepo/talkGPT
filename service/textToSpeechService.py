import pyaudio
import wave
import os
import whisper
import whisper
import pyaudio
import time
import threading
from pydub import AudioSegment
import openai
import pyttsx3
from pydub.playback import play
import utils.VAConstants as constants
from pydub.effects import normalize
from utils.logger import Logger
from service.googleTTS import GoogleTTS
import configparser
import asyncio
from threading import Thread

logger = Logger("textToSpeechService")


class textToSpeechService:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.use_local_tts = eval(self.config["General"]["useLocalTTS"])
        # Create a logger instance with the name "textToSpeechService"

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate", 210
        )  # adjust the rate to 150 words per minute for the default, 210 if you are using post Processing
        self.engine.setProperty("volume", 0.7)  # adjust the volume to 70%
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty(
            "voice", self.voices[1].id
        )  # select the second available voice
        self.googleTTS = GoogleTTS()

    def post_process_audio(self, audio_path, pitch_correction, normalization):
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)

        # Apply pitch correction if enabled
        if pitch_correction:
            audio = audio._spawn(
                audio.raw_data,
                overrides={
                    "frame_rate": int(
                        audio.frame_rate * (2.0**pitch_correction / 13.0)
                    )
                },
            )
            audio = audio.set_frame_rate(audio.frame_rate)

        # Apply normalization if enabled
        if normalization:
            audio = normalize(audio)

        # Export the processed audio to the same file
        audio.export(audio_path, format="wav")

    def text_to_speech(self, text):
        if self.use_local_tts:
            audio_path = constants.OUTPUT_FOLDER + "response.wav"
            self.engine.save_to_file(text, audio_path)
            self.engine.runAndWait()
            # Apply post-processing to the audio file
            self.post_process_audio(
                audio_path, pitch_correction=3.37, normalization=True
            )

            # Load the WAV file
            audio = AudioSegment.from_wav(audio_path)

            # Play the audio
            play(audio)
        else:
            self.googleTTS.synthesize_text(text)

    def utility_response(self, text):
        if self.use_local_tts:
            audio_path = constants.OUTPUT_FOLDER + "utility_response.wav"
            self.engine.save_to_file(text, audio_path)
            self.engine.runAndWait()
            # Apply post-processing to the audio file
            self.post_process_audio(
                audio_path, pitch_correction=3.37, normalization=True
            )
            # Load the WAV file
            audio = AudioSegment.from_wav(audio_path)

            # Play the audio
            play(audio)
        else:
            self.googleTTS.synthesize_text(text)

    def text_to_speech_async(self, text):
        # Create a new thread to run the text_to_speech method in the background
        thread = Thread(target=self.text_to_speech, args=(text,))
        thread.start()
        return thread
