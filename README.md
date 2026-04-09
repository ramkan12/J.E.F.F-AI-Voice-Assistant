# J.E.F.F Voice Assistant

**Just an Extremely Friendly Fella** - A Python voice assistant with speech recognition and natural language processing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- 🎤 Voice recognition using Google Speech API
- 🔊 Text-to-speech responses
- 🤖 **Optional AI integration** - Smart responses for any question (free with Groq!)
- 🌤️ Weather updates (OpenWeatherMap)
- 🧮 Basic calculations
- ⏰ Time and date queries
- 🌐 Web browsing commands
- 📝 Simple reminders
- 😄 Jokes and conversation

## 🌐 Try It Online!

**Live Web Demo:** [Coming Soon - Deploy to see it here!]

Experience J.E.F.F in your browser with full voice capabilities - no installation needed!

## Quick Start

### Option 1: Web Interface (Recommended)

```bash
# Clone and install
git clone https://github.com/ramkan12/J.E.F.F-Voice-Assistant.git
cd J.E.F.F-Voice-Assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run web app
python web_app.py
```

Open http://localhost:5000 and interact with J.E.F.F through:
- 🎤 Voice input (click and speak)
- ⌨️ Text input (type commands)
- 🔊 Voice responses

### Option 2: Command Line

```bash
# Text mode (no microphone)
python jeff_cli.py

# Voice mode (requires microphone)
python main.py
```

## Setup

### 1. Get API Key (Free)

- Sign up at [OpenWeatherMap](https://openweathermap.org/api)
- Copy your API key
- Add it to `config/config.yaml`

### 2. Install Dependencies

**macOS:**
```bash
brew install portaudio mpg123
pip install -r requirements.txt
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev mpg123
pip install -r requirements.txt
```

## Usage

### Text Mode
```bash
python jeff_cli.py
```
Type commands instead of speaking - great for testing!

### Voice Mode
```bash
python main.py
```
Speak naturally into your microphone.

### Example Commands

- "Hello" - Greeting
- "What time is it?" - Current time
- "What's the weather?" - Weather info
- "Tell me a joke" - Random joke
- "Calculate 25 times 4" - Math
- "Remind me to buy milk" - Set reminder
- "Open YouTube" - Launch website
- "Help" - List commands
- "Goodbye" - Exit

## Project Structure

```
├── src/jeff/          # Main package
│   ├── core.py       # Assistant logic
│   ├── speech.py     # Voice I/O
│   ├── commands.py   # Command handlers
│   └── utils.py      # Utilities
├── config/           # Configuration
├── examples/         # Usage examples
├── tests/           # Tests
├── main.py          # Voice mode
└── jeff_cli.py      # Text mode
```

## Configuration

Edit `config/config.yaml`:

```yaml
weather_api_key: "your_key_here"
default_city: "Tampa"
log_level: "INFO"
pause_threshold: 1.0
```

### Enable AI Features (Optional)

Make J.E.F.F much smarter with free AI integration:

1. Get a free API key from [Groq](https://console.groq.com) (no credit card needed!)
2. Update `config/config.yaml`:
```yaml
use_ai_fallback: true  # Enable AI
groq_api_key: "your_groq_key_here"
```

Now J.E.F.F can answer **any question**:
- "What's the capital of France?"
- "Explain quantum physics simply"
- "Write me a haiku about coding"
- "What should I make for dinner?"

**How it works:** Known commands (time, weather, jokes) run instantly. Unknown questions get sent to AI for smart responses!

## Extending

Add custom commands by extending the `CommandHandler` class:

```python
from jeff import VoiceAssistant
from jeff.commands import CommandHandler

class MyCommands(CommandHandler):
    def my_feature(self):
        return "Custom response"

assistant = VoiceAssistant()
assistant.command_handler = MyCommands()
assistant.run()
```

See `examples/` for more.

## Troubleshooting

**Microphone not working?**
- Check system permissions
- Try text mode: `python jeff_cli.py`

**PyAudio install fails?**
- macOS: `brew install portaudio && pip install pyaudio`
- Linux: `sudo apt-get install portaudio19-dev`

**Weather not working?**
- Add API key to `config/config.yaml`
- Wait 10-15 min after creating key for activation

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

Built with Google Speech Recognition, gTTS, and OpenWeatherMap API.
