"""
J.E.F.F (Just an Extremely Friendly Fella)
A Python-based voice assistant with natural language processing capabilities.
"""

__version__ = "2.0.0"
__author__ = "Riham Khan"

from .core import VoiceAssistant
from .commands import CommandHandler
from .speech import SpeechEngine

__all__ = ["VoiceAssistant", "CommandHandler", "SpeechEngine"]
