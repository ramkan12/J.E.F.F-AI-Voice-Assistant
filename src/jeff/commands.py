"""
Command handlers for J.E.F.F voice assistant.
"""

import datetime
import random
import webbrowser
import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)


class CommandHandler:
    """Handles various voice commands and their execution."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize command handler.

        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or {}
        self.reminders_file = self.config.get('reminders_file', 'reminders.txt')

        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the programmer quit his job? He didn't get arrays!",
            "Why do Python programmers prefer snakes? Because they don't like Java!",
            "What's a computer's favorite snack? Microchips!",
            "Why was the JavaScript developer sad? Because he didn't know how to null his feelings!",
            "What do you call a programmer from Finland? Nerdic!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
        ]

        self.greetings = [
            "Hello there!",
            "Hi! How can I help you?",
            "Hey! What can I do for you today?",
            "Greetings! Ready to assist you!"
        ]

        self.status_responses = [
            "I'm doing great, thanks for asking!",
            "All systems operational and ready to help!",
            "I'm fantastic! How can I assist you today?",
            "Running smoothly and ready for your commands!"
        ]

        logger.info("Command handler initialized")

    def get_greeting(self) -> str:
        """Return a random greeting."""
        return random.choice(self.greetings)

    def get_status(self) -> str:
        """Return a random status response."""
        return random.choice(self.status_responses)

    def get_time(self) -> str:
        """Get current time."""
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        logger.debug(f"Time requested: {current_time}")
        return f"The current time is {current_time}"

    def get_date(self) -> str:
        """Get current date."""
        today = datetime.date.today()
        formatted_date = today.strftime('%A, %B %d, %Y')
        logger.debug(f"Date requested: {formatted_date}")
        return f"Today is {formatted_date}"

    def tell_joke(self) -> str:
        """Tell a random joke."""
        joke = random.choice(self.jokes)
        logger.debug("Joke requested")
        return joke

    def calculate(self, expression: str) -> str:
        """
        Perform basic calculations.

        Args:
            expression: Mathematical expression to evaluate

        Returns:
            Result of calculation or error message
        """
        try:
            # Clean up the expression
            expression = expression.replace("calculate", "").replace("math", "").strip()

            # Safety check - only allow numbers and basic operators
            allowed_chars = "0123456789+-*/(). "
            if all(char in allowed_chars for char in expression):
                result = eval(expression)
                logger.info(f"Calculation: {expression} = {result}")
                return f"The answer is {result}"
            else:
                logger.warning(f"Invalid calculation attempt: {expression}")
                return "Sorry, I can only do basic math calculations with numbers and operators."
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return "Sorry, I couldn't calculate that. Please check your expression."

    def get_weather(self, city: Optional[str] = None) -> str:
        """
        Get current weather information.

        Args:
            city: City name (uses default from config if not provided)

        Returns:
            Weather information or error message
        """
        try:
            api_key = self.config.get('weather_api_key')
            if not api_key or api_key == 'your_api_key_here':
                return "Weather service requires an API key. Please add your OpenWeatherMap API key to the config file."

            city = city or self.config.get('default_city', 'Tampa')
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']

                logger.info(f"Weather requested for {city}")
                return (f"The current temperature in {city} is {temp} degrees Celsius, "
                       f"feels like {feels_like} degrees, with {description}. "
                       f"Humidity is at {humidity}%.")
            else:
                logger.warning(f"Weather API error: {data.get('message', 'Unknown error')}")
                return "Sorry, I couldn't get the weather information for that location."

        except requests.exceptions.Timeout:
            logger.error("Weather API timeout")
            return "Weather service is taking too long to respond."
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return "Weather service is currently unavailable."

    def set_reminder(self, reminder_text: str) -> str:
        """
        Set a simple reminder by saving to file.

        Args:
            reminder_text: Text of the reminder

        Returns:
            Confirmation message or error
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(self.reminders_file, "a") as file:
                file.write(f"{timestamp}: {reminder_text}\n")
            logger.info(f"Reminder set: {reminder_text}")
            return f"Reminder set: {reminder_text}"
        except Exception as e:
            logger.error(f"Error setting reminder: {e}")
            return "Sorry, I couldn't set that reminder."

    def open_website(self, url: str, name: str) -> str:
        """
        Open a website in the default browser.

        Args:
            url: URL to open
            name: Display name of the website

        Returns:
            Confirmation message
        """
        try:
            webbrowser.open(url)
            logger.info(f"Opened website: {url}")
            return f"Opening {name}"
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return f"Sorry, I couldn't open {name}"

    def get_help(self) -> str:
        """Return help information about available commands."""
        return """I can help you with the following:
        - Opening websites (YouTube, Google, Reddit)
        - Telling the time and date
        - Weather updates (requires API key)
        - Telling jokes
        - Basic calculations
        - Setting reminders
        - General conversation

        Just speak naturally! For example:
        'What time is it?'
        'Tell me a joke'
        'Calculate 25 times 4'
        'Open YouTube'
        'Remind me to call mom'"""

    def get_name_info(self) -> str:
        """Return information about J.E.F.F's name."""
        return "I'm J.E.F.F, which stands for Just an Extremely Friendly Fella! I'm here to make your day easier."

    def ask_ai(self, question: str) -> Optional[str]:
        """
        Use AI for general questions (fallback when no command matches).

        Args:
            question: The user's question

        Returns:
            AI response or None if AI is disabled/unavailable
        """
        # Check if AI is enabled in config
        if not self.config.get('use_ai_fallback', False):
            return None

        try:
            from groq import Groq

            api_key = self.config.get('groq_api_key')
            if not api_key or api_key == 'your_groq_api_key_here':
                logger.warning("AI fallback enabled but no valid Groq API key found")
                return None

            # Initialize Groq client
            client = Groq(api_key=api_key)

            # Create chat completion
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are J.E.F.F (Just an Extremely Friendly Fella), a helpful and friendly voice assistant. Keep responses concise (2-3 sentences max) and conversational."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                model="llama-3.1-8b-instant",  # Fast, free model
                temperature=0.7,
                max_tokens=150,
            )

            response = chat_completion.choices[0].message.content
            logger.info(f"AI response generated for: {question}")
            return response

        except ImportError:
            logger.error("Groq library not installed. Install with: pip install groq")
            return None
        except Exception as e:
            logger.error(f"AI request failed: {e}")
            return None
