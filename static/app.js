// J.E.F.F Web App - Client-side JavaScript

// DOM Elements
const voiceBtn = document.getElementById('voiceBtn');
const voiceStatus = document.getElementById('voiceStatus');
const textInput = document.getElementById('textInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messages');
const listeningIndicator = document.getElementById('listeningIndicator');
const browserNotice = document.getElementById('browserNotice');

// Speech Recognition Setup
let recognition = null;
let isListening = false;

// Check browser support for Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isListening = true;
        voiceBtn.classList.add('listening');
        voiceStatus.textContent = 'Listening...';
        listeningIndicator.style.display = 'flex';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('Recognized:', transcript);
        sendCommand(transcript, true);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isListening = false;
        voiceBtn.classList.remove('listening');
        voiceStatus.textContent = 'Click to Speak';
        listeningIndicator.style.display = 'none';

        if (event.error === 'no-speech') {
            addMessage("I didn't hear anything. Please try again.", 'assistant');
        } else if (event.error === 'not-allowed') {
            addMessage("Microphone access denied. Please enable microphone permissions.", 'assistant');
        }
    };

    recognition.onend = () => {
        isListening = false;
        voiceBtn.classList.remove('listening');
        voiceStatus.textContent = 'Click to Speak';
        listeningIndicator.style.display = 'none';
    };
} else {
    // Browser doesn't support speech recognition
    browserNotice.style.display = 'block';
    voiceBtn.disabled = true;
    voiceBtn.style.opacity = '0.5';
}

// Text-to-Speech Setup
const synth = window.speechSynthesis;
let selectedVoice = null;

// Get available voices and select a good male voice
function loadVoices() {
    const voices = synth.getVoices();

    // Try to find enhanced/premium male voices first, then fallback to any male voice
    const maleVoices = voices.filter(voice =>
        voice.name.toLowerCase().includes('male') ||
        voice.name.toLowerCase().includes('david') ||
        voice.name.toLowerCase().includes('james') ||
        voice.name.toLowerCase().includes('daniel') ||
        voice.name.toLowerCase().includes('fred')
    );

    // Prefer English voices
    const englishMaleVoices = maleVoices.filter(voice =>
        voice.lang.startsWith('en-')
    );

    // Select the best available voice
    if (englishMaleVoices.length > 0) {
        // Prefer "Enhanced" or "Premium" voices
        selectedVoice = englishMaleVoices.find(v =>
            v.name.includes('Enhanced') || v.name.includes('Premium')
        ) || englishMaleVoices[0];
    } else if (maleVoices.length > 0) {
        selectedVoice = maleVoices[0];
    }

    if (selectedVoice) {
        console.log('Selected voice:', selectedVoice.name);
    } else {
        console.log('No male voice found, using default');
    }
}

// Load voices when available
if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = loadVoices;
}
loadVoices();

function speak(text) {
    if (synth) {
        // Cancel any ongoing speech
        synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);

        // Use selected male voice
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }

        // Settings for smoother, more masculine sound
        utterance.rate = 1.1;       // Slightly faster for natural flow
        utterance.pitch = 0.85;     // Lower pitch for masculine sound
        utterance.volume = 1.0;

        synth.speak(utterance);
    }
}

// Event Listeners
voiceBtn.addEventListener('click', () => {
    if (recognition && !isListening) {
        try {
            recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }
});

sendBtn.addEventListener('click', () => {
    const command = textInput.value.trim();
    if (command) {
        sendCommand(command, false);
        textInput.value = '';
    }
});

textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const command = textInput.value.trim();
        if (command) {
            sendCommand(command, false);
            textInput.value = '';
        }
    }
});

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Send command to backend
async function sendCommand(command, useVoice) {
    // Add user message
    addMessage(command, 'user');

    try {
        // Show loading
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant';
        loadingDiv.innerHTML = '<div class="message-content">Thinking...</div>';
        loadingDiv.id = 'loading-message';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Send request to backend
        const response = await fetch('/api/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command })
        });

        // Remove loading message
        const loading = document.getElementById('loading-message');
        if (loading) {
            loading.remove();
        }

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.error) {
            addMessage('Sorry, there was an error: ' + data.error, 'assistant');
        } else {
            addMessage(data.response, 'assistant');

            // Speak response if voice was used
            if (useVoice) {
                speak(data.response);
            }
        }

    } catch (error) {
        console.error('Error:', error);

        // Remove loading message if still there
        const loading = document.getElementById('loading-message');
        if (loading) {
            loading.remove();
        }

        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    }
}

// Initialize
console.log('J.E.F.F Voice Assistant loaded');
console.log('Speech Recognition supported:', !!recognition);
console.log('Speech Synthesis supported:', !!synth);
