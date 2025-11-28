
import streamlit as st
import os
import google.generativeai as genai

# --- Load and Configure API Key ---
api_key = os.environ.get("GOOGLE_API_KEY")  # Try to get from environment variable first (for deployment)

if not api_key: # If not found in environment, try from .env file for local development
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key.strip() == "GOOGLE_API_KEY":
                        api_key = value.strip()
                        break

if api_key:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        st.stop()

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- App Title and Description ---
st.title("🤖 Gemini Chatbot")
st.caption("A friendly AI companion powered by the Gemini API and Streamlit")

# --- Initialize Chat History in Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Previous Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Send Button ---
prompt = st.chat_input("What would you like to talk about?")

if prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Call Gemini API with conversation history ---
    try:
        if not api_key:
            st.error("Google API key not found. Please create a `.env` file with `GOOGLE_API_KEY=YOUR_KEY`.")
            st.stop()

        # Construct conversation history for the API
        api_history = []
        for msg in st.session_state.messages:
            # The API expects 'model' for the assistant's role
            role = "model" if msg["role"] == "assistant" else msg["role"]
            api_history.append({'role': role, 'parts': [{'text': msg['content']}]})

        # Prepend a system instruction if it's the start of the conversation
        if len(api_history) == 1:
            system_instruction = {
                'role': 'user',
                'parts': [{
                    'text': "You are a friendly and helpful AI assistant. Your goal is to have a pleasant and engaging conversation. Let's start."
                }]
            }
            # Insert system instruction before the first user prompt
            api_history.insert(0, system_instruction)

        model = genai.GenerativeModel('models/gemini-pro-latest')
        
        # The entire history, including the latest prompt, is sent
        response = model.generate_content(api_history)

        bot_response = response.text

        # Add bot response to chat history and display it
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        # --- Error Handling ---
        error_message = f"An error occurred with the Gemini API: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})


# --- Bonus Feature: Clear Chat Button ---
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun() # Rerun the app to reflect the cleared history
