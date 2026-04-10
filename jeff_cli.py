#!/usr/bin/env python3
"""
J.E.F.F Text-Only Version
A text-based interface for testing without voice hardware.
"""

import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core import VoiceAssistant
from src.utils import load_config, setup_logging


class TextOnlyAssistant(VoiceAssistant):
    """Text-only version of the voice assistant for testing."""

    def __init__(self, config=None):
        """Initialize text-only assistant."""
        super().__init__(config)

        # Override speech engine methods for text-only mode
        self.speech_engine.speak = self._text_speak
        self.speech_engine.listen = self._text_listen

    def _text_speak(self, text: str, language: str = 'en') -> None:
        """Print text instead of speaking."""
        print(f"J.E.F.F: {text}")

    def _text_listen(self, timeout=None) -> str:
        """Get text input instead of voice."""
        try:
            command = input("You: ").lower().strip()
            return command
        except (EOFError, KeyboardInterrupt):
            return "goodbye"


def main():
    """Main entry point for text-only version."""
    # Setup logging
    setup_logging(level='INFO')

    # Load configuration
    config = load_config('config/config.yaml')

    print("=" * 60)
    print("J.E.F.F - Text-Only Mode")
    print("=" * 60)
    print("\nType your commands instead of speaking them.")
    print("Try: 'hello', 'what time', 'tell joke', 'help', or 'bye'\n")

    # Create and run text-only assistant
    assistant = TextOnlyAssistant(config)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nShutting down. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
