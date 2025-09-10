# J.E.F.F (Just an Extremely Friendly Fella) - Enhanced Voice Assistant
from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib
import datetime
import random
import requests
import json

def talkToMe(audio):
    """Text-to-speech function"""
    print(f"J.E.F.F: {audio}")
    tts = gTTS(text=audio, lang='en')
    tts.save('audio.mp3')
    os.system('mpg123 audio.mp3')

def myCommand():
    """Listen for voice commands"""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for your command...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f'You said: {command}')
        return command

    except sr.UnknownValueError:
        talkToMe("Sorry, I didn't catch that. Could you repeat?")
        return myCommand()
    except sr.RequestError:
        talkToMe("Sorry, there seems to be an issue with the speech service.")
        return ""

def get_weather():
    """Get current weather information"""
    try:
        # You would need to get a free API key from OpenWeatherMap
        api_key = "your_api_key_here"
        city = "Tampa"  # Default city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp} degrees Celsius with {description}"
        else:
            return "Sorry, I couldn't get the weather information right now."
    except:
        return "Weather service is currently unavailable."

def tell_joke():
    """Tell a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the programmer quit his job? He didn't get arrays!",
        "Why do Python programmers prefer snakes? Because they don't like Java!",
        "What's a computer's favorite snack? Microchips!",
        "Why was the JavaScript developer sad? Because he didn't know how to null his feelings!"
    ]
    return random.choice(jokes)

def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return f"The current time is {current_time}"

def get_date():
    """Get current date"""
    today = datetime.date.today()
    return f"Today is {today.strftime('%A, %B %d, %Y')}"

def calculate(expression):
    """Perform basic calculations"""
    try:
        # Remove "calculate" from the expression
        expression = expression.replace("calculate", "").strip()
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = "0123456789+-*/(). "
        if all(char in allowed_chars for char in expression):
            result = eval(expression)
            return f"The answer is {result}"
        else:
            return "Sorry, I can only do basic math calculations."
    except:
        return "Sorry, I couldn't calculate that."

def set_reminder(reminder_text):
    """Set a simple reminder (saves to file)"""
    try:
        with open("reminders.txt", "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            file.write(f"{timestamp}: {reminder_text}\n")
        return f"Reminder set: {reminder_text}"
    except:
        return "Sorry, I couldn't set that reminder."

def assistant(command):
    """Main assistant logic"""
    
    # Greeting responses
    if any(word in command for word in ['hello', 'hi', 'hey']):
        greetings = ["Hello there!", "Hi! How can I help you?", "Hey! What can I do for you?"]
        talkToMe(random.choice(greetings))
    
    # Web browsing
    elif 'open reddit python' in command:
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        url = 'https://www.reddit.com/r/Python/'
        webbrowser.get(chrome_path).open(url)
        talkToMe('Opening Reddit Python for you')
    
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        talkToMe('Opening YouTube')
    
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
        talkToMe('Opening Google')
    
    # Time and date
    elif 'what time' in command or 'current time' in command:
        talkToMe(get_time())
    
    elif 'what date' in command or 'today' in command:
        talkToMe(get_date())
    
    # Weather
    elif 'weather' in command:
        talkToMe(get_weather())
    
    # Jokes
    elif 'joke' in command or 'funny' in command:
        talkToMe(tell_joke())
    
    # Calculations
    elif 'calculate' in command or 'math' in command:
        talkToMe(calculate(command))
    
    # Reminders
    elif 'remind me' in command:
        reminder_text = command.replace('remind me to', '').replace('remind me', '').strip()
        talkToMe(set_reminder(reminder_text))
    
    # General responses
    elif any(phrase in command for phrase in ['how are you', 'what\'s up', 'how\'s it going']):
        responses = [
            "I'm doing great, thanks for asking!",
            "All systems operational and ready to help!",
            "I'm fantastic! How can I assist you today?"
        ]
        talkToMe(random.choice(responses))
    
    elif 'your name' in command:
        talkToMe("I'm J.E.F.F, which stands for Just an Extremely Friendly Fella!")
    
    elif 'goodbye' in command or 'bye' in command:
        talkToMe("Goodbye! Have a great day!")
        return False
    
    # Email (simplified - you'd need to update with proper credentials)
    elif 'email' in command:
        talkToMe('Email feature is currently disabled for security reasons.')
    
    # Help command
    elif 'help' in command:
        help_text = """I can help you with: opening websites, telling time and date, 
                      weather updates, telling jokes, basic calculations, setting reminders, 
                      and general conversation. Just speak naturally!"""
        talkToMe(help_text)
    
    else:
        talkToMe("Sorry, I'm not sure how to help with that. Try saying 'help' for available commands.")
    
    return True

# Main program
if __name__ == "__main__":
    talkToMe("Hello! I'm J.E.F.F, your voice assistant. I'm ready for your commands!")
    
    while True:
        try:
            continue_running = assistant(myCommand())
            if not continue_running:
                break
        except KeyboardInterrupt:
            talkToMe("Shutting down. Goodbye!")
            break
        except Exception as e:
            talkToMe("Something went wrong, but I'm still here to help!")