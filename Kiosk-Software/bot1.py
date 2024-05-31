import streamlit as st
from googletrans import Translator
import requests
from pydub import AudioSegment
from pydub.playback import play
import threading
import os

RAPIDAPI_KEY = "24a6ebe7d2msh31370e8035ac91bp1d14adjsn5f6c48f9f363"  # Replace with your RapidAPI key

# Set the path to your 'static' folder
AUDIO_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))  # Replace with the actual path to your 'static' folder

# Function to translate text using Google Text-to-Speech Translator
def translate_to_selected_language(text, selected_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=selected_language)
    return translated_text.text

# def play_announcement_audio(language_code):
#     audio_file_path = os.path.join(AUDIO_FOLDER_PATH, f'Dindigul_{language_code.lower()}.mp3')
    
    try:
        audio = AudioSegment.from_file(audio_file_path, format="mp3")
        play(audio)
    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Function to translate text using Google Text-to-Speech Translator
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to get PNR status
def get_pnr_status(pnr_number, language_code, selected_language):
    url = "https://irctc1.p.rapidapi.com/api/v3/getPNRStatus"
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
    }
    translated_pnr = translate_text(str(pnr_number), 'en')  # Translate PNR to English
    params = {
        'pnrNumber': translated_pnr,
    }
    response = requests.get(url, headers=headers, params=params)

    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        result = response.json()

        if 'data' in result and 'Pnr' in result['data']:
            # Translate the result to the selected language
            translated_result = translate_to_selected_language(str(result), selected_language)
            return translated_result  # Return the entire result JSON
        elif 'error' in result and result['error']:
            st.error(f"Error: {result['error']['message']}")
        else:
            st.warning("PNR status information is incomplete or not available.")
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
        st.error(f"HTTP Response Content: {response.text}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error: {err}")

def get_live_train_status(train_number, language_code, selected_language):
    url = "https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus"
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
    }
    translated_train_number = translate_text(str(train_number), 'en')  # Translate train number to English
    params = {
        'trainNo': translated_train_number,
    }
    response = requests.get(url, headers=headers, params=params)

    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        result = response.json()

        if 'data' in result and 'train_number' in result['data']:
            # Translate the result to the selected language
            translated_result = translate_to_selected_language(str(result['data']['train_name']), selected_language)
            translated_result1 = translate_to_selected_language(str(result['data']['train_number']), selected_language)
            translated_result2 = translate_to_selected_language(str(result['data']['seo_train_name']), selected_language)
            translated_result4 = translate_to_selected_language(str(result['data']['destination']), selected_language)
            return  translated_result, translated_result1, translated_result2, translated_result4
        elif 'error' in result and result['error']:
            st.warning(f"Warning: {result['error']['message']}")
        else:
            st.warning("Live train status information is incomplete or not available.")

    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
        st.error(f"HTTP Response Content: {response.text}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error: {err}")

# Function to get ChatGPT response
def get_chatgpt_response(user_message, selected_language):
    url = "https://chatgpt-42.p.rapidapi.com/matag2"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "365d347764msh72f1281f5fcdde9p12de25jsnd54b68134ad5",
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "system_prompt": "",
        "temperature": 0.5,
        "top_k": 50,
        "top_p": 0.9,
        "max_tokens": 200
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        chatgpt_result = response.json().get("result", "")
        # Translate the result to the selected language
        translated_result = translate_to_selected_language(str(chatgpt_result), selected_language)
        return translated_result
    else:
        st.error(f"Error: {response.status_code}, {response.text}")

def play_audio_thread(language_code):
    play_announcement_audio(language_code)

# Main content based on user option
# Main content based on user option
st.title("Aawaz")
# Language selection
selected_language = st.sidebar.selectbox("Select Language", ["मराठी", "English", "தமிழ்", " हिंदी "])

# Options based on language
if selected_language == "मराठी":
    language_code = "mr"
elif selected_language == "English":
    language_code = "en"
    audio_file_path = os.path.join(AUDIO_FOLDER_PATH, 'Dindigul_english.mp3')
    st.audio(audio_file_path, format="audio/mp3", start_time=0)
elif selected_language == "தமிழ்":
    language_code = "ta"
elif selected_language == " हिंदी ":
    language_code = "hi"

# Main content based on user option
option = st.sidebar.selectbox("Select an option", ("PNR Status", "Live Train Status", "Trains Between Stations", "Recent Announcement", "Ask Anything"))

# Translate the entire Streamlit page
# if st.button("Translate", key="translate_button"):
#     st.text("Translating... This may take a moment.")
#     st.caching.clear_cache()
#     st.experimental_rerun()
# Create a placeholder for the announcement option
# announcement_placeholder = st.empty()

if option == "PNR Status":
    st.subheader(translate_text("PNR Status", language_code))
    pnr_number = st.text_input(translate_text("Enter PNR Number", language_code))
    if st.button(translate_text("Check PNR Status", language_code)):
        result = get_pnr_status(pnr_number, language_code, selected_language)
        if result:
            st.subheader(translate_text("Result:", language_code))
            st.success(f"PNR Status Result: {result}")
        else:
            st.warning(translate_text("Unexpected response from the API. Please check your input.", language_code))

elif option == "Live Train Status":
    st.subheader("Live Train Status")
    train_number = st.text_input(translate_text("Enter Train Number", language_code))
    if st.button(translate_text("Check Live Train Status", language_code)):
        result = get_live_train_status(train_number, language_code, selected_language)
        if result:
            st.subheader(translate_text("Result:", language_code))
            st.success(f"Live Train Status Result: {result}")
        else:
            st.warning(translate_text("Unexpected response from the API. Please check your input.", language_code))

elif option == "Trains Between Stations":
    st.subheader(translate_text("Trains Between Stations", language_code))
    from_station_code = st.text_input(translate_text("Enter From Station Code", language_code))
    to_station_code = st.text_input(translate_text("Enter To Station Code", language_code))
    date_of_journey = st.date_input(translate_text("Select Date of Journey", language_code))

    if st.button(translate_text("Check Trains Between Stations", language_code)):
        user_query = st.text_input(translate_text("Ask a question about the trains between stations", language_code))
        if user_query:
            openai_response = get_chatgpt_response(user_query, selected_language)
            st.subheader(translate_text("OpenAI Response:", language_code))
            st.write(openai_response)

elif option == "Ask Anything":
    st.subheader(translate_text("Ask Anything Related to Indian Railways", language_code))
    user_question = st.text_input(translate_text("Ask a question", language_code))
    if st.button(translate_text("Get Answer", language_code)):
        chatgpt_response = get_chatgpt_response(user_question, selected_language)
        st.subheader(translate_text("ChatGPT Response:", language_code))
        st.write(chatgpt_response)
        

if option == "Recent Announcement":
    st.subheader(translate_text("Recent Announcement", language_code))
    
    # Display language selection box for recent announcement
    selected_language_recent = st.selectbox("Select Language", ["Marathi", "English", "Tamil", "Hindi"])

    # play_button_recent = st.button(f"Play Announcement in {selected_language_recent}", key="play_button_recent")
    # if play_button_recent:
    #     play_announcement_audio(selected_language_recent.lower())

    # Show audio file after selecting language
    audio_file_path_recent = os.path.join(AUDIO_FOLDER_PATH, f'Dindigul_{selected_language_recent.lower()}.mp3')
    st.audio(audio_file_path_recent, format="audio/mp3")