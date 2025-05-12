import requests
import json
import time
from config import CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsuranceLLM:
    """Class to interact with the Hugging Face LLM model for insurance assistance."""
    
    def __init__(self):
        self.api_key = CONFIG["huggingface_api_key"]
        self.model_id = CONFIG["model_id"]
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.timeout = CONFIG["api_timeout"]
        self.max_retries = CONFIG["max_retries"]
        
    def _prepare_prompt(self, query, country, language, insurance_type=None):
        """Prepare a prompt for the LLM based on user inputs."""
        
        # Format the query with context
        base_prompt = f"""
You are an AI assistant specialized in insurance for {country}. 
Respond in {language}.

"""
        if insurance_type:
            base_prompt += f"Focus on {insurance_type} insurance.\n\n"
        
        base_prompt += f"User query: {query}\n\nRespond with helpful, accurate information about insurance:"
        
        return base_prompt
    
    def generate_response(self, query, country, language, insurance_type=None, chat_history=None):
        """Generate a response from the LLM for an insurance query."""
        
        for attempt in range(self.max_retries):
            try:
                prompt = self._prepare_prompt(query, country, language, insurance_type)
                
                # Add chat history context if available
                if chat_history and len(chat_history) > 0:
                    context = "Previous conversation:\n"
                    for entry in chat_history[-3:]:  # Include last 3 exchanges for context
                        context += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n"
                    prompt = context + "\n\n" + prompt
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 512,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "do_sample": True
                    },
                    "options": {
                        "wait_for_model": True  # This tells the API to wait if model is loading
                    }
                }
                
                logger.info(f"Sending request to HuggingFace API for model: {self.model_id} (Attempt {attempt+1}/{self.max_retries})")
                response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=self.timeout)
                
                # Handle different response status codes
                if response.status_code == 200:
                    result = response.json()
                    # Extract the generated text from the response
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "")
                        # Clean up response - remove the prompt part if it's included
                        if generated_text.startswith(prompt):
                            generated_text = generated_text[len(prompt):].strip()
                        return generated_text
                    return CONFIG["fallback_responses"]["default"]
                
                elif response.status_code == 503:
                    # Model is still loading, wait and retry
                    logger.warning(f"Model still loading. Waiting before retry. Status: {response.status_code}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    
                    # If this is the last retry, return a fallback response
                    if attempt == self.max_retries - 1:
                        return self._generate_fallback_response(query, country, insurance_type)
                    
                    # Otherwise wait and retry
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except requests.exceptions.Timeout:
                logger.error("Request timed out")
                time.sleep(2 ** attempt)  # Exponential backoff
                if attempt == self.max_retries - 1:
                    return CONFIG["fallback_responses"]["timeout"]
                
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._generate_fallback_response(query, country, insurance_type)
                time.sleep(2 ** attempt)  # Exponential backoff
                
        # If we've exhausted all retries
        return self._generate_fallback_response(query, country, insurance_type)
    
    def _generate_fallback_response(self, query, country, insurance_type=None):
        """Generate a fallback response when the API fails."""
        # This is a simple fallback mechanism when the API is unavailable
        
        # Basic responses for different insurance types
        basic_responses = {
            "auto": f"Auto insurance in {country} typically covers liability for accidents, damage to your vehicle, and medical expenses. Policies can include collision, comprehensive, and personal injury protection.",
            "home": f"Home insurance in {country} usually covers damage to your property from events like fire, theft, and certain natural disasters. It often includes liability coverage for accidents on your property.",
            "health": f"Health insurance in {country} helps cover medical expenses like doctor visits, hospital stays, and prescription medications. Coverage types and costs vary based on the specific plan.",
            "life": f"Life insurance in {country} provides financial protection for your beneficiaries after your death. Policies can be term (for a specific period) or permanent (for your entire life).",
            "travel": f"Travel insurance in {country} typically covers trip cancellations, medical emergencies abroad, lost luggage, and other travel-related issues. Costs vary based on destination and coverage level.",
            "business": f"Business insurance in {country} protects companies from various risks including property damage, liability claims, and business interruption. Coverage needs vary by industry and company size.",
            "liability": f"Liability insurance in {country} covers costs if you're legally responsible for damages or injuries to others. It's important for both individuals and businesses to protect their assets.",
            "pet": f"Pet insurance in {country} helps cover veterinary expenses for illness or injury to your pet. Plans vary in coverage and cost based on your pet's age, breed, and existing conditions."
        }
        
        if insurance_type and insurance_type in basic_responses:
            return basic_responses[insurance_type]
        
        # If no specific insurance type or not found in our mappings
        return f"Insurance in {country} offers protection against various risks, from health problems to property damage. Different policies cover different needs. To get specific advice, consider what you want to protect and consult with insurance professionals."

    def get_insurance_info(self, insurance_type, country, language):
        """Get general information about a specific insurance type."""
        prompt = f"""
Provide a brief overview of {insurance_type} insurance in {country}.
Include key coverage details, typical costs, and important considerations.
Respond in {language}.
"""
        return self.generate_response(prompt, country, language, insurance_type)