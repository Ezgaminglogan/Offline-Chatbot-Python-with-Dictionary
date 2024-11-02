import eel
import re
import spacy
import maths  # Import the updated maths module

# Set path to Brave browser
eel.browsers.set_path('chrome', 'C:/Program Files/BraveSoftware/Brave-Browser-Nightly/Application/brave.exe')

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Global variables
current_language = "english"
context = {}

# Function to determine intent from user message using spaCy
def determine_intent(message):
    doc = nlp(message)
    intents = list(maths.responses.keys())  # Get intents from the dictionary
    for token in doc:
        if token.lemma_ in intents:
            return token.lemma_
    # Check for exact matches, considering lowercase
    message_lower = message.lower()
    for intent in intents:
        if intent in message_lower:
            return intent
    return None

# Function to get chatbot response
@eel.expose
def get_response(message):
    global current_language, context
    message_lower = message.lower()

    # Language-switching logic
    if "speak filipino" in message_lower:
        current_language = "filipino"
        return "Switched to Filipino! 🇵🇭"
    elif "speak cebuano" in message_lower or "speak bisaya" in message_lower:
        current_language = "cebuano"
        return "Switched to Cebuano! 🇵🇭"
    elif "speak english" in message_lower:
        current_language = "english"
        return "Switched to English! 🇬🇧"
    elif "speak japanese" in message_lower:
        current_language = "japanese"
        return "Switched to Japanese! 🇯🇵"
    elif "speak spanish" in message_lower:
        current_language = "spanish"
        return "Switched to Spanish! 🇪🇸"
    elif "speak french" in message_lower:
        current_language = "french"
        return "Switched to French! 🇫🇷"

    # Check if the message is a math expression
    if re.match(maths.math_pattern, message_lower):
        return maths.evaluate_math(message_lower)

    # Determine intent
    intent = determine_intent(message_lower)
    if intent:
        bot_response = maths.fetch_response(intent, current_language)
        context[intent] = message_lower  # Update context for the intent
    else:
        bot_response = "Sorry, I didn't quite catch that. Could you rephrase? 🤔"

    return bot_response

# Initialize Eel and start the application
eel.init('web')
eel.start('index.html', mode='chrome', size=(1000, 750), suppress_error=True)
