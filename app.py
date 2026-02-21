from ctypes.util import test
import streamlit as st
import requests
import json
from streamlit_option_menu import option_menu
from sarvamai import SarvamAI
import base64
import os
from dotenv import load_dotenv
load_dotenv()

with st.sidebar:
    st.header("Chat with Sarvam AI")
    user_name = st.text_input("Enter your name", label_visibility="hidden", placeholder="Enter your name")
    
    selected = option_menu(
        menu_title=None,  
        options=["Text to Speech", "Hello"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"display": "none"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "color": "grey",
                "margin": "5px", 
                "--hover-color": "transparent",
                "border": "1px grey solid"
            },
            "nav-link-selected": {
                "background-color": "#ff4b4b",
                "font-size": "16px",
                "text-align": "right",
                "border": "none",
                "font-weight": "normal",
                "color": "white"
            },
        }
    )

try:
    SARVAM_API_KEY = st.secrets.get("SARVAM_API_KEY")
except:
    SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if selected == "Text to Speech":
    st.title("Text to Speech:")
    # st.write("Convert your text into speech")
    
    sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY,)

    col1, col2 = st.columns([3, 1]) 

    with col1:
        user_input = st.text_input(
            "", 
            placeholder="1. Enter the text to be converted to Speech",
            label_visibility="collapsed"
        )
    
        speech_response_container = st.container()

    # user_input = user_input.lower()

    with col2:
        generate_speech_button = st.button("Generate Speech", type="primary")
    if generate_speech_button:
        if user_input:
            response = sarvam_client.text_to_speech.convert(
                text=user_input,
                target_language_code="en-IN",
                speaker="ratan",
                pace=0.9,
                speech_sample_rate=48000,
                enable_preprocessing=True,
                model="bulbul:v3"
            )

            audio_base64 = response.audios[0]
            audio_bytes = base64.b64decode(audio_base64)

            with speech_response_container:
                st.audio(audio_bytes, format="audio/wav")

    col3, col4 = st.columns([3, 1])

    with col3:
        user_query = st.text_input(
            "", 
            placeholder="2. Enter your query",
            label_visibility="collapsed"
        )
        if user_query:
            if user_name:
                st.write(f"**{user_name}**" + ": " + user_query)
            else:
                st.write("**User:** " + user_query)
        ai_response_container = st.container()
    with col4:
        ask_ai_button = st.button("Ask AI", type="primary")
    if ask_ai_button:
        if user_query:
            url = "https://api.sarvam.ai/v1/chat/completions"
            headers = {
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "messages": [
                    {"role": "system", "content": "You'll be acting as a helpful assistant and provide the response for the queries, this response is later given to Sarvam AI and the speech is generated with the response you've given. So, give me the response in a way any TTS AI can convert this to Speech easily. That's why don't use any emojis, logos, symbols etc,."},
                    {"role": "user", "content": user_query}
                ],
                "model": "sarvam-m"
            }
            text_response = requests.post(url, headers=headers, json=data)
            text_response = text_response.json()
            try:
                text_response = text_response['choices'][0]['message']['content']
            except (KeyError, IndexError):
                text_response = "I'm sorry, I couldn't generate a response."

            audio_response = sarvam_client.text_to_speech.convert(
                text=text_response,
                target_language_code="en-IN",
                speaker="ratan",
                pace=0.9,
                speech_sample_rate=48000,
                enable_preprocessing=True,
                model="bulbul:v3"
            )

            
            audio_base64 = audio_response.audios[0]
            audio_bytes = base64.b64decode(audio_base64)
                
            if audio_bytes:
                with ai_response_container:
                    st.markdown(f"**AI:** {text_response}")
                    st.audio(audio_bytes, format="audio/wav")



