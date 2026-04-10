#!/usr/bin/env python3
"""
J.E.F.F Web Application
Flask-based web interface for the voice assistant
"""

import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.commands import CommandHandler
from src.utils import load_config, setup_logging

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Setup logging
setup_logging(level='INFO')

# Load configuration
config = load_config('config/config.yaml')

# Initialize command handler
command_handler = CommandHandler(config)


def process_command(command_text: str) -> str:
    """
    Process a command and return the response text.

    Args:
        command_text: The command to process

    Returns:
        Response text
    """
    command = command_text.lower().strip()

    if not command:
        return "I didn't catch that. Please try again."

    # Status check (check this FIRST to avoid greeting conflicts)
    if any(phrase in command for phrase in ['how are you', "what's up", "how's it going", 'how are things', 'how you doing']):
        return command_handler.get_status()

    # Greeting (only if NOT asking how I am)
    elif any(word in command for word in ['hello', 'hi', 'hey', 'greetings']) and 'how' not in command:
        return command_handler.get_greeting()

    # Name inquiry
    elif 'your name' in command or 'who are you' in command:
        return command_handler.get_name_info()

    # Time
    elif 'what time' in command or 'current time' in command or 'time is it' in command:
        return command_handler.get_time()

    # Date
    elif 'what date' in command or 'what day' in command or "today's date" in command:
        return command_handler.get_date()

    # Weather
    elif 'weather' in command:
        return command_handler.get_weather()

    # Jokes
    elif 'joke' in command or 'funny' in command or 'make me laugh' in command:
        return command_handler.tell_joke()

    # Calculations
    elif 'calculate' in command or 'math' in command or 'plus' in command or 'minus' in command:
        return command_handler.calculate(command)

    # Reminders
    elif 'remind me' in command:
        reminder_text = command.replace('remind me to', '').replace('remind me', '').strip()
        return command_handler.set_reminder(reminder_text)

    # Help
    elif 'help' in command or 'what can you do' in command or 'capabilities' in command:
        return command_handler.get_help()

    # Email (disabled for security)
    elif 'email' in command or 'send' in command and '@' in command:
        return "I don't have email capabilities for security reasons, but I can help you draft a message or assist with other tasks!"

    # Unknown command - try AI fallback
    else:
        ai_response = command_handler.ask_ai(command)
        if ai_response:
            return ai_response
        else:
            return "Sorry, I'm not sure how to help with that. Try saying 'help' for available commands."


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/command', methods=['POST'])
def handle_command():
    """Handle command requests from the frontend."""
    try:
        data = request.get_json()
        command = data.get('command', '')

        if not command:
            return jsonify({'error': 'No command provided'}), 400

        response = process_command(command)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'J.E.F.F is running!'})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
