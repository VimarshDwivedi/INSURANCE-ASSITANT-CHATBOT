import streamlit as st
import logging
import time
from config import CONFIG
from model import InsuranceLLM
from ui_components import InsuranceChatbotUI
from insurance_logic import InsuranceAssistant

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Initialize components
    ui = InsuranceChatbotUI()
    llm = InsuranceLLM()
    assistant = InsuranceAssistant()
    
    # Initialize session state variables if they don't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_insurance_type' not in st.session_state:
        st.session_state.current_insurance_type = None
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    
    # Display UI header
    ui.display_header()
    
    # Display country and language settings
    country, language = ui.display_settings()
    
    # Display chat history
    ui.display_chat_history(st.session_state.chat_history)
    
    # Display insurance type selection buttons
    selected_type = ui.display_insurance_type_buttons()
    if selected_type:
        st.session_state.loading = True
        st.session_state.current_insurance_type = selected_type
        
        # Rerun to show loading state
        st.rerun()
    
    # If we're in loading state after selecting an insurance type
    if st.session_state.loading and st.session_state.current_insurance_type:
        with st.spinner("Getting insurance information..."):
            try:
                insurance_type_name = CONFIG["insurance_types"][st.session_state.current_insurance_type].split()[1]
                # When an insurance type is selected, display info about it
                insurance_info = llm.get_insurance_info(
                    insurance_type_name,
                    country, 
                    language
                )
                
                # Format with regulatory information
                formatted_info = assistant.format_response(
                    insurance_info,
                    st.session_state.current_insurance_type,
                    country
                )
                
                # Add this to chat history as if user asked about this insurance type
                user_msg = f"Tell me about {insurance_type_name} insurance in {country}."
                st.session_state.chat_history.append({
                    "user": user_msg,
                    "assistant": formatted_info
                })
                
                # Reset loading state
                st.session_state.loading = False
                st.rerun()  # Refresh to display the new message
                
            except Exception as e:
                logger.error(f"Error getting insurance info: {str(e)}")
                st.error(f"Error getting insurance information. Please try again.")
                st.session_state.loading = False
    
    # Display user input area
    user_input = ui.display_input_area()
    
    # Display clear chat button
    if ui.clear_chat_button():
        st.session_state.chat_history = []
        st.session_state.current_insurance_type = None
        st.rerun()
    
    # Process user input
    if user_input:
        # Add user message to chat history immediately
        temp_history = st.session_state.chat_history + [{"user": user_input, "assistant": ""}]
        
        # Show temporary chat history with user message
        ui.display_chat_history(temp_history)
        
        # Show loading message
        with st.spinner("Thinking..."):
            # Detect insurance type from message if not already set
            if not st.session_state.current_insurance_type:
                detected_type = assistant.determine_insurance_type(user_input)
                st.session_state.current_insurance_type = detected_type
            
            try:
                # Generate response
                response = llm.generate_response(
                    user_input, 
                    country, 
                    language, 
                    st.session_state.current_insurance_type,
                    st.session_state.chat_history
                )
                
                # Format response with regulatory information
                formatted_response = assistant.format_response(
                    response, 
                    st.session_state.current_insurance_type, 
                    country
                )
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": user_input,
                    "assistant": formatted_response
                })
                
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                # Use fallback response in case of error
                error_response = CONFIG["fallback_responses"]["api_error"]
                st.session_state.chat_history.append({
                    "user": user_input,
                    "assistant": error_response
                })
            
            # Refresh UI to show the new message
            st.rerun()
    
    # Display audio button
    ui.display_audio_button()

    # Show API key warning if not set
    if not CONFIG["huggingface_api_key"]:
        st.warning("⚠️ Hugging Face API key not set! Please add your API key to the .env file.")

if __name__ == "__main__":
    main()