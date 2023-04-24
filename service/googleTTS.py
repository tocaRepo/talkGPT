from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
from utils.logger import Logger

# Create a logger instance with the name "GoogleTTS"
logger = Logger("GoogleTTS")


class GoogleTTS:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-J",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def synthesize_text(self, text, output_file="processing/response.mp3"):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        logger.info(f'Audio content written to file "{output_file}"')
        # Load the audio file using PyDub
        audio = AudioSegment.from_file(output_file, format="mp3")
        # Play the audio file
        play(audio)
