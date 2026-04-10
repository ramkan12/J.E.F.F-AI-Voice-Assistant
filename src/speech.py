"""
Speech recognition and text-to-speech functionality for J.E.F.F.
"""

import logging
from typing import Optional
from gtts import gTTS
import speech_recognition as sr
import os

logger = logging.getLogger(__name__)


class SpeechEngine:
    """Handles speech recognition and text-to-speech operations."""

    def __init__(self, audio_file: str = "audio.mp3", pause_threshold: float = 1.0):
        """
        Initialize the speech engine.

        Args:
            audio_file: Path to save temporary audio files
            pause_threshold: Seconds of silence before phrase is considered complete
        """
        self.audio_file = audio_file
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = pause_threshold
        logger.info("Speech engine initialized")

    def speak(self, text: str, language: str = 'en') -> None:
        """
        Convert text to speech and play it.

        Args:
            text: Text to speak
            language: Language code for speech synthesis
        """
        try:
            print(f"J.E.F.F: {text}")
            tts = gTTS(text=text, lang=language)
            tts.save(self.audio_file)
            os.system(f'mpg123 {self.audio_file}')
            logger.debug(f"Spoke: {text}")
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            print(f"J.E.F.F: {text}")  # Fallback to text output

    def listen(self, timeout: Optional[int] = None) -> Optional[str]:
        """
        Listen for voice command and convert to text.

        Args:
            timeout: Maximum time to wait for a phrase to start (seconds)

        Returns:
            Recognized command text or None if recognition failed
        """
        try:
            with sr.Microphone() as source:
                print("Listening for your command...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout)

            command = self.recognizer.recognize_google(audio).lower()
            print(f'You said: {command}')
            logger.info(f"Recognized command: {command}")
            return command

        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return self.listen(timeout=timeout)

        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            self.speak("Sorry, there seems to be an issue with the speech service.")
            return None

        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return None

        except Exception as e:
            logger.error(f"Unexpected error during listening: {e}")
            return None

    def cleanup(self) -> None:
        """Remove temporary audio files."""
        try:
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
                logger.debug(f"Removed temporary file: {self.audio_file}")
        except Exception as e:
            logger.error(f"Error cleaning up audio file: {e}")
