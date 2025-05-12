import streamlit as st
from config import CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsuranceChatbotUI:
    """Class to handle UI components for the insurance chatbot."""
    
    def display_header(self):
        """Display the app header and description."""
        st.set_page_config(
            page_title=CONFIG["app_title"],
            page_icon="🤖",
            layout="wide"
        )
        
        st.title(f"🤖 {CONFIG['app_title']}")
        st.markdown(CONFIG["app_description"])
        
        # Add a divider
        st.markdown("---")
    
    def display_settings(self):
        """Display country and language selection dropdowns."""
        # Create two columns for settings
        col1, col2 = st.columns(2)
        
        # Country selection in first column
        with col1:
            country = st.selectbox(
                "Select your country:",
                options=CONFIG["countries"],
                index=CONFIG["countries"].index(CONFIG["default_country"]) if CONFIG["default_country"] in CONFIG["countries"] else 0
            )
        
        # Language selection in second column
        with col2:
            language = st.selectbox(
                "Select your preferred language:",
                options=CONFIG["supported_languages"],
                index=CONFIG["supported_languages"].index(CONFIG["default_language"]) if CONFIG["default_language"] in CONFIG["supported_languages"] else 0
            )
        
        # Add a small gap
        st.markdown("##")
        
        return country, language
    
    def display_insurance_type_buttons(self):
        """Display buttons for selecting insurance types."""
        st.markdown("### Select Insurance Type (optional)")
        
        # Create a flexible grid of buttons using columns
        columns = st.columns(4)  # 4 buttons per row
        
        selected_type = None
        for i, (type_id, type_name) in enumerate(CONFIG["insurance_types"].items()):
            with columns[i % 4]:
                if st.button(type_name, key=f"btn_{type_id}"):
                    selected_type = type_id
        
        # Add space after buttons
        st.markdown("##")
        
        return selected_type
    
    def display_chat_history(self, chat_history):
        """Display the chat history."""
        st.markdown("### Chat")
        
        # Create a container for chat messages
        chat_container = st.container()
        
        with chat_container:
            for message in chat_history:
                # User message with custom styling
                st.markdown(
                    f"""
                    <div style='background-color: #e6f7ff; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                        <p><strong>You:</strong> {message['user']}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Assistant message with custom styling
                st.markdown(
                    f"""
                    <div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
                        <p><strong>Assistant:</strong> {message['assistant'].replace('\n', '<br>')}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
    
    def display_input_area(self):
        """Display the text input area for user messages."""
        user_input = st.text_area("Ask me about insurance:", height=100)
        
        # Add a submit button to send the message
        submit = st.button("Ask")
        
        if submit and user_input:
            return user_input
        
        return None
    
    def display_audio_button(self):
        """Display a button for audio messages (placeholder for future functionality)."""
        # This is a placeholder for future audio input functionality
        st.markdown("##")
        audio_col1, audio_col2 = st.columns([1, 4])
        
        with audio_col1:
            st.button("🎤", help="Voice input (Coming soon)")
        
        with audio_col2:
            st.markdown("*Voice input coming soon*")
    
    def display_loading_message(self):
        """Display a loading message while waiting for API response."""
        with st.spinner("Thinking..."):
            st.info("The AI is generating a response. This may take a moment.")
    
    def display_error_message(self, error_message):
        """Display an error message."""
        st.error(f"Error: {error_message}")
    
    def clear_chat_button(self):
        """Display a button to clear the chat history."""
        if st.button("Clear Chat", key="clear_chat"):
            return True
        return False