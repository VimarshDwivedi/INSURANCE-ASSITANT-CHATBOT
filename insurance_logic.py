import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsuranceAssistant:
    """Class that handles insurance-specific logic and processing."""
    
    def __init__(self):
        self.chat_history = []
        
    def add_to_history(self, user_message: str, assistant_response: str) -> None:
        """Add an exchange to the chat history."""
        self.chat_history.append({
            "user": user_message,
            "assistant": assistant_response
        })
        # Keep history to reasonable size
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)
    
    def get_history(self) -> List[Dict[str, str]]:
        """Return the current chat history."""
        return self.chat_history
    
    def clear_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []
    
    def determine_insurance_type(self, message: str) -> Optional[str]:
        """
        Analyze the user message to determine which insurance type they're asking about.
        Returns the insurance type or None if it can't be determined.
        """
        message = message.lower()
        
        # Map of keywords to insurance types
        insurance_keywords = {
            "auto": ["car", "vehicle", "auto", "automobile", "driving", "driver", "crash"],
            "home": ["house", "home", "property", "apartment", "condo", "dwelling", "building"],
            "health": ["health", "medical", "doctor", "hospital", "illness", "sick", "injury"],
            "life": ["life", "death", "dying", "beneficiary", "dependent"],
            "travel": ["travel", "trip", "vacation", "journey", "overseas", "abroad"],
            "business": ["business", "company", "commercial", "liability", "professional"],
            "liability": ["liability", "sued", "lawsuit", "legal", "responsibility"],
            "pet": ["pet", "dog", "cat", "animal", "veterinarian", "vet"]
        }
        
        # Check for keywords in message
        for insurance_type, keywords in insurance_keywords.items():
            if any(keyword in message for keyword in keywords):
                return insurance_type
        
        return None
    
    def get_relevant_regulations(self, insurance_type: str, country: str) -> str:
        """
        Return information about insurance regulations for the given type and country.
        This is a placeholder - in production, this would connect to a database or API.
        """
        # This is simplified mock data - in a real application, this would be more extensive
        regulations = {
            "Canada": {
                "auto": "In Canada, auto insurance is regulated provincially. Each province has its own minimum coverage requirements.",
                "home": "Home insurance is not legally required in Canada, but most mortgage lenders require it.",
                "health": "Canada has a public health system (Medicare), but many Canadians also have private health insurance for services not covered.",
                "life": "Life insurance in Canada is regulated by the Office of the Superintendent of Financial Institutions (OSFI).",
                "default": "Insurance in Canada is regulated at both the federal and provincial levels."
            },
            "United States": {
                "auto": "Auto insurance requirements vary by state in the US. Most states require liability insurance.",
                "health": "Health insurance in the US is regulated under the Affordable Care Act, though requirements vary by state.",
                "default": "Insurance in the US is primarily regulated at the state level."
            },
            "India": {
                "auto": "In India, third-party auto insurance is mandatory under the Motor Vehicles Act.",
                "home": "Home insurance is not mandatory in India, but is recommended especially in disaster-prone areas.",
                "health": "India has both government health insurance schemes like Ayushman Bharat and private health insurance options.",
                "life": "Life insurance in India is regulated by the Insurance Regulatory and Development Authority of India (IRDAI).",
                "default": "Insurance in India is regulated by the Insurance Regulatory and Development Authority of India (IRDAI)."
            },
            "default": {
                "default": "Insurance regulations vary by country and region."
            }
        }
        
        # Get country-specific regulations or default
        country_regs = regulations.get(country, regulations["default"])
        
        # Get insurance-type specific regulations or default for the country
        return country_regs.get(insurance_type, country_regs.get("default", regulations["default"]["default"]))
    
    def format_response(self, llm_response: str, insurance_type: Optional[str], country: str) -> str:
        """Format the final response to include relevant regulatory information if appropriate."""
        formatted_response = llm_response
        
        # Add regulatory information if we have an insurance type
        if insurance_type:
            regulations = self.get_relevant_regulations(insurance_type, country)
            formatted_response += f"\n\n**Regulatory Note**: {regulations}"
        
        return formatted_response