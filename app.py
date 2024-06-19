import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get the Gemini API key from the environment variables
API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the Gemini API client
genai.configure(api_key=API_KEY)

# Create the model with specific generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

st.title("Gemini ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = chat_session.send_message(prompt)
    response_text = response.text

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
