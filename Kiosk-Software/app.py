from flask import Flask, render_template, request, url_for
import mysql.connector
import os
import time
import pyttsx3 

from translate import recognize_and_translate

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Database configuration for connecting sql dataset
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aawaz2023sih@19",
    database="newlanguage_db"
)

def get_translations():
    cursor = db.cursor(dictionary=True)

    # Fetch translations from the 'TranslationsTable'
    cursor.execute("SELECT * FROM TranslationsTable WHERE keyword IN ('Emergency', 'FAQ', 'Select option from below', 'PNR', 'Recent Announcement', 'Helpline', 'Station Information', 'PNR Status Checker', 'Home', 'Enter PNR Number', 'Check Status', 'Speak', 'Enter language code', 'Translate and Speak', 'Submit', 'Or use voice input', 'Start Voice Input', 'Live Train Status', 'Train Between Stations')")
    translations_data = cursor.fetchall()

    # Close the cursor to avoid 'Unread result found' error
    cursor.close()

    translations_dict = {}
    for translation in translations_data:
        keyword = translation['keyword']
        translations_dict[keyword] = {
            'marathi_translation': translation['marathi_translation'],
            'hindi_translation': translation['hindi_translation'],
            'english_translation': translation['english_translation'],
            'tamil_translation': translation['tamil_translation'],
            'french_translation': translation['french_translation'],
            'german_translation': translation['german_translation']
        }

    return translations_dict

def perform_translation(language_code):
    # the translation logic here and return the filename of the translated audio
    # For demonstration purposes,assume the filename is 'translated_audio.mp3'
    translated_audio_file = 'translated_audio.mp3'
    return translated_audio_file

def voice_output(message, rate=150, gender='female'):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust the speech rate as needed
    engine.setProperty('voice', f'com.apple.speech.synthesis.voice.{gender}')  # Adjust for different platforms
    engine.say(message)
    engine.runAndWait()

# Home route with welcome message
@app.route('/')
def home():
    # Voice output welcome message
    welcome_message = "Welcome to Aawaz one stop solution"
    voice_output(welcome_message)
    return render_template('home.html')

@app.route('/lang', methods=['POST'])
def lang():

    welcome_message = "Please select your language."
    voice_output(welcome_message, rate=120)
    return render_template('lang.html')

@app.route('/options', methods=['POST'])
def options():

    selected_language = request.form.get('language')
    translations = get_translations()
        # Voice output indicating the selected language
    selection_message = f" {selected_language}."
    voice_output(selection_message, rate=160)
    return render_template('options.html', translations=translations, selected_language=selected_language)

@app.route('/pnr')
def pnr():
    selected_language = request.args.get('language', 'english')  # Set a default language english
    translations = get_translations()
    return render_template('pnr.html', translations=translations, selected_language=selected_language)

@app.route('/info')
def info():
    selected_language = request.args.get('language', 'english')  # Set a default language ienglish
    translations = get_translations()
    return render_template('info.html', translations=translations, selected_language=selected_language)

def perform_translation(language_code):
    # Implement the translation logic here and return the filename of the translated audio
    # For demonstration purposes, let's assume the filename is 'translated_audio.mp3'
    translated_audio_file = 'translated_audio.mp3'
    
    # Save the translated audio file (wee can replace this with your actual saving logic)
    # we can use the recognize_and_translate function from translate.py
    recognize_and_translate('static/recorded_audio.wav', language_code)
    
    return translated_audio_file

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        # will Get language code from the form submission
        language_code = request.form['language']

        # here we Perform translation and get the filename of the translated audio
        translated_audio_file = perform_translation(language_code)

        # Introduce a delay to needs to wait for the translation to complete
        time.sleep(5)  #  we can Adjust this delay as needed 

        # code will Redirect to the recent page after 5 seconds
        return render_template('recent.html', target_url=url_for('recent', language=language_code))

    translations = get_translations()
    selected_language = request.args.get('language', 'english')  

    return render_template('translate.html', translations=translations, selected_language=selected_language)

@app.route('/recent')
def recent():
    selected_language = request.args.get('language', 'english')  
    translations = get_translations()
    return render_template('recent.html', translations=translations, selected_language=selected_language)

@app.route('/TrainBetnStations')
def TrainBetnStations():
    selected_language = request.args.get('language', 'english')  
    translations = get_translations()
    return render_template('TrainBetnStations.html', translations=translations, selected_language=selected_language)

@app.route('/TrainLiveSts')
def TrainLiveSts():
    selected_language = request.args.get('language', 'english')  
    translations = get_translations()
    return render_template('TrainLiveSts.html', translations=translations, selected_language=selected_language)

if __name__ == '__main__':
    app.run(debug=True)
