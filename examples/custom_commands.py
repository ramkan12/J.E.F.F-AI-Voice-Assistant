#!/usr/bin/env python3
"""
Example: Adding custom commands to J.E.F.F
Shows how to extend J.E.F.F with your own commands
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core import VoiceAssistant
from src.commands import CommandHandler
from src.utils import load_config, setup_logging


class CustomCommandHandler(CommandHandler):
    """Extended command handler with custom commands."""

    def get_system_info(self) -> str:
        """Get basic system information."""
        import platform
        return (f"You're running {platform.system()} {platform.release()} "
                f"on {platform.machine()}")

    def motivational_quote(self) -> str:
        """Return a motivational quote."""
        import random
        quotes = [
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Code is like humor. When you have to explain it, it's bad. - Cory House",
        ]
        return random.choice(quotes)


class CustomVoiceAssistant(VoiceAssistant):
    """Extended voice assistant with custom commands."""

    def __init__(self, config=None):
        super().__init__(config)
        # Replace with our custom command handler
        self.command_handler = CustomCommandHandler(config)

    def process_command(self, command: str) -> bool:
        """Process commands including custom ones."""

        # Check for custom commands first
        if 'system info' in command or 'my system' in command:
            response = self.command_handler.get_system_info()
            self.speech_engine.speak(response)
            return True

        if 'motivate me' in command or 'motivation' in command:
            response = self.command_handler.motivational_quote()
            self.speech_engine.speak(response)
            return True

        # Fall back to default commands
        return super().process_command(command)


def main():
    """Main function."""
    setup_logging(level='INFO')
    config = load_config('../config/config.yaml')

    print("=" * 60)
    print("J.E.F.F with Custom Commands")
    print("=" * 60)
    print("\nTry these custom commands:")
    print("  - 'What's my system info?'")
    print("  - 'Motivate me'")
    print("\nAll standard commands still work too!\n")

    assistant = CustomVoiceAssistant(config)
    assistant.run()


if __name__ == "__main__":
    main()
