import re
import json
import math

# Load conversation responses and multilingual responses from JSON file with UTF-8 encoding
with open('web/dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Use .lower() to access responses correctly
responses = {k.lower(): v for k, v in data.get("responses", {}).items()}
multilingual_responses = {
    lang: {k.lower(): v for k, v in responses.items()}
    for lang, responses in data.get("multilingual_responses", {}).items()
}

# Regular expression for basic arithmetic operations (supports more operations)
math_pattern = r'^[0-9\.\+\-\*/\(\)\s\^]+$'

# Enhanced math function for PEMDAS and advanced operations
def evaluate_math(expression):
    try:
        # Replace '^' with '**' for exponentiation
        expression = expression.replace('^', '**')
        
        # Safeguard eval by restricting to math operations and functions
        result = eval(expression, {"__builtins__": None}, {
            "math": math,
            "pow": pow,          # Exponentiation
            "sqrt": math.sqrt,    # Square root
            "log": math.log,      # Natural logarithm
            "log10": math.log10,  # Base-10 logarithm
            "sin": math.sin,      # Sine
            "cos": math.cos,      # Cosine
            "tan": math.tan,      # Tangent
            "pi": math.pi,        # PI constant
            "e": math.e           # Euler's number
        })
        
        # Return result with precision to handle floats cleanly
        return str(round(result, 10)) if isinstance(result, float) else str(result)
    except Exception:
        return "Invalid math expression."

# Function to fetch response from the JSON-based dictionary based on intent
def fetch_response(intent, language="english"):
    intent_lower = intent.lower()
    if language in multilingual_responses and intent_lower in multilingual_responses[language]:
        return multilingual_responses[language][intent_lower]
    return responses.get(intent_lower, "I don't have a response for that.")
