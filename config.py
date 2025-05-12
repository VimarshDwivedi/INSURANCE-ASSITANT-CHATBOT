import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
CONFIG = {
    "huggingface_api_key": os.getenv("HUGGINGFACE_API_KEY"),
    "model_id": "QuantFactory/Open-Insurance-LLM-Llama3-8B-GGUF",
    "app_title": "AI Insurance Chatbot",
    "app_description": "Welcome! Pick your country, choose a language, and describe your insurance-related query. We're here to assist you!",
    "default_language": "English",
    "default_country": "India",  # Changed default to India since that was in your example
    "insurance_types": {
        "auto": "🚗 Auto",
        "home": "🏠 Home",
        "health": "🏥 Health",
        "life": "❤️ Life",
        "travel": "✈️ Travel",
        "business": "💼 Business",
        "liability": "⚠️ Liability",
        "pet": "🐾 Pet"
    },
    "supported_languages": [
        "English", "French", "Spanish", "German", "Chinese", 
        "Japanese", "Arabic", "Russian", "Portuguese", "Hindi"
    ],
    "countries": [
        "India", "Canada", "United States", "United Kingdom", "Australia", 
        "Germany", "France", "Japan", "China", "Brazil"
    ],
    # API configuration
    "api_timeout": 60,  # Timeout in seconds
    "max_retries": 3,   # Number of retries if API fails
    "fallback_responses": {
        "api_error": "I'm having trouble connecting to my knowledge base. Please try again in a moment.",
        "timeout": "It's taking longer than expected to process your request. Please try a simpler question or try again later.",
        "default": "I couldn't generate a proper response for your query. Could you please rephrase your question?"
    }
}