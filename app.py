from ctypes.util import test
import streamlit as st
from openai import OpenAI
from streamlit_option_menu import option_menu
from sarvamai import SarvamAI
import base64
import os
from dotenv import load_dotenv
load_dotenv()

with st.sidebar:
    st.header("Chat with Sarvam AI")
    
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

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if selected == "Text to Speech":
    st.title("Text to Speech:")
    st.write("Convert your text into speech")
    
    sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY,)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    user_input = st.text_input("Enter the text to be converted to Speech")
    # user_input = user_input.lower()

    if st.button("Generate Speech"):
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

            st.audio(audio_bytes, format="audio/wav")

    user_query = st.text_input("Enter your query")
    if st.button("Ask AI"):
        if user_query:

            ai_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You'll be acting as a helpful assistant and provide the response for the queries, this response is later given to Sarvam AI and the speech is generated with the response you've given. So, give me the response in a way any TTS AI can convert this to Speech easily. That's why don't use any emojis, logos, symbols etc,."},
                    {"role": "user", "content": user_query}
                ]
            )
            text_response = ai_response.choices[0].message.content

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
                st.markdown(text_response)
                st.audio(audio_bytes, format="audio/wav")



