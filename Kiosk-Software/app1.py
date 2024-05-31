# app.py
import os
import time
from flask import Flask, render_template, request, redirect, url_for
from record_and_save_audio import record_and_save_audio
from translate import recognize_and_translate

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('record_audio.html')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    #it saves  the filename for the WAV file
    filename = os.path.join("static", "recorded_audio.wav")

    # Run the function to record and save audio by user
    try:
        record_and_save_audio(filename)
        recording_message = "Recording saved successfully!"
    except Exception as e:
        print(f"Error recording audio: {e}")
        recording_message = "Error occurred while saving the recording."

    # Return the recording message in file
    return render_template('record_audio.html', recording_message=recording_message)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    # Remaining translation code
    if request.method == 'POST':
        # Get language code from the form submission
        language_code = request.form['language']

        # Introduce a delay to wait for the translation to complete added delay
        time.sleep(5)

        # Render the translate_and_speak.html page with a success message
        return render_template('translate.html', success_message="Language preference updated successfully!")

    return render_template('translate.html')

if __name__ == '__main__':
    app.run(debug=True)
