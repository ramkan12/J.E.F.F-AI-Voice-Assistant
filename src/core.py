"""
Core voice assistant functionality for J.E.F.F.
"""

import logging
from typing import Optional, Dict, Any
from .speech import SpeechEngine
from .commands import CommandHandler

logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Main voice assistant class that coordinates speech and command processing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the voice assistant.

        Args:
            config: Configuration dictionary with settings and API keys
        """
        self.config = config or {}
        self.speech_engine = SpeechEngine()
        self.command_handler = CommandHandler(config)
        self.running = False
        logger.info("Voice assistant initialized")

    def process_command(self, command: str) -> bool:
        """
        Process a voice command and execute appropriate action.

        Args:
            command: The command string to process

        Returns:
            True to continue running, False to shutdown
        """
        if not command:
            return True

        logger.info(f"Processing command: {command}")

        # Greeting
        if any(word in command for word in ['hello', 'hi', 'hey', 'greetings']):
            self.speech_engine.speak(self.command_handler.get_greeting())

        # Status check
        elif any(phrase in command for phrase in ['how are you', "what's up", "how's it going", 'how are things']):
            self.speech_engine.speak(self.command_handler.get_status())

        # Name inquiry
        elif 'your name' in command or 'who are you' in command:
            self.speech_engine.speak(self.command_handler.get_name_info())

        # Time
        elif 'what time' in command or 'current time' in command or 'time is it' in command:
            self.speech_engine.speak(self.command_handler.get_time())

        # Date
        elif 'what date' in command or 'what day' in command or "today's date" in command:
            self.speech_engine.speak(self.command_handler.get_date())

        # Weather
        elif 'weather' in command:
            self.speech_engine.speak(self.command_handler.get_weather())

        # Jokes
        elif 'joke' in command or 'funny' in command or 'make me laugh' in command:
            self.speech_engine.speak(self.command_handler.tell_joke())

        # Calculations
        elif 'calculate' in command or 'math' in command or 'plus' in command or 'minus' in command:
            self.speech_engine.speak(self.command_handler.calculate(command))

        # Reminders
        elif 'remind me' in command:
            reminder_text = command.replace('remind me to', '').replace('remind me', '').strip()
            self.speech_engine.speak(self.command_handler.set_reminder(reminder_text))

        # Website opening
        elif 'open youtube' in command:
            self.speech_engine.speak(self.command_handler.open_website('https://www.youtube.com', 'YouTube'))

        elif 'open google' in command:
            self.speech_engine.speak(self.command_handler.open_website('https://www.google.com', 'Google'))

        elif 'open reddit' in command:
            url = 'https://www.reddit.com/r/Python/' if 'python' in command else 'https://www.reddit.com'
            self.speech_engine.speak(self.command_handler.open_website(url, 'Reddit'))

        elif 'open github' in command:
            self.speech_engine.speak(self.command_handler.open_website('https://www.github.com', 'GitHub'))

        # Help
        elif 'help' in command or 'what can you do' in command or 'capabilities' in command:
            self.speech_engine.speak(self.command_handler.get_help())

        # Exit
        elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
            self.speech_engine.speak("Goodbye! Have a great day!")
            return False

        # Unknown command - try AI fallback
        else:
            # Try AI for general conversation
            ai_response = self.command_handler.ask_ai(command)

            if ai_response:
                self.speech_engine.speak(ai_response)
            else:
                # AI disabled or failed - use default message
                self.speech_engine.speak(
                    "Sorry, I'm not sure how to help with that. Try saying 'help' for available commands."
                )

        return True

    def run(self) -> None:
        """Start the voice assistant main loop."""
        self.running = True
        logger.info("Starting voice assistant")

        welcome_message = "Hello! I'm J.E.F.F, your voice assistant. I'm ready for your commands!"
        self.speech_engine.speak(welcome_message)

        try:
            while self.running:
                command = self.speech_engine.listen()
                if command:
                    should_continue = self.process_command(command)
                    if not should_continue:
                        self.running = False
                        break

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.speech_engine.speak("Shutting down. Goodbye!")

        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            self.speech_engine.speak("Something went wrong, but I'm shutting down gracefully.")

        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources before shutdown."""
        logger.info("Cleaning up resources")
        self.speech_engine.cleanup()
