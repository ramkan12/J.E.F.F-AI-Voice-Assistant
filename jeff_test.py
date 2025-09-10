# J.E.F.F (Just an Extremely Friendly Fella) - Text-Only Version for Testing
import datetime
import random
import webbrowser
import os

def talkToMe(audio):
    """Text-to-speech function (text-only for now)"""
    print(f"J.E.F.F: {audio}")

def myCommand():
    """Get text input instead of voice for testing"""
    command = input("You: ").lower()
    return command

def get_time():
    """Get current time"""
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    return f"The current time is {current_time}"

def get_date():
    """Get current date"""
    today = datetime.date.today()
    return f"Today is {today.strftime('%A, %B %d, %Y')}"

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

def assistant(command):
    """Main assistant logic"""
    
    # Greeting responses
    if any(word in command for word in ['hello', 'hi', 'hey']):
        greetings = ["Hello there!", "Hi! How can I help you?", "Hey! What can I do for you?"]
        talkToMe(random.choice(greetings))
    
    # Web browsing
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        talkToMe('Opening YouTube')
    
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
        talkToMe('Opening Google')
    
    # Time and date
    elif 'time' in command:
        talkToMe(get_time())
    
    elif 'date' in command:
        talkToMe(get_date())
    
    # Jokes
    elif 'joke' in command:
        talkToMe(tell_joke())
    
    # Calculations
    elif 'calculate' in command:
        talkToMe(calculate(command))
    
    # General responses
    elif any(phrase in command for phrase in ['how are you', 'what\'s up']):
        responses = [
            "I'm doing great, thanks for asking!",
            "All systems operational and ready to help!",
            "I'm fantastic! How can I assist you today?"
        ]
        talkToMe(random.choice(responses))
    
    elif 'name' in command:
        talkToMe("I'm J.E.F.F, which stands for Just an Extremely Friendly Fella!")
    
    elif any(word in command for word in ['goodbye', 'bye', 'quit', 'exit']):
        talkToMe("Goodbye! Have a great day!")
        return False
    
    # Help command
    elif 'help' in command:
        help_text = """I can help you with: opening websites, telling time and date, 
                      telling jokes, basic calculations, and general conversation. 
                      Try: 'open youtube', 'what time', 'tell joke', 'calculate 5+3'"""
        talkToMe(help_text)
    
    else:
        talkToMe("Sorry, I'm not sure how to help with that. Try saying 'help' for available commands.")
    
    return True

# Main program
if __name__ == "__main__":
    talkToMe("Hello! I'm J.E.F.F, your text assistant. Type your commands below!")
    talkToMe("Try: 'hello', 'what time', 'tell joke', 'open youtube', 'help', or 'bye'")
    
    while True:
        try:
            continue_running = assistant(myCommand())
            if not continue_running:
                break
        except KeyboardInterrupt:
            talkToMe("Shutting down. Goodbye!")
            break