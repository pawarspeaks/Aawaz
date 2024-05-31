# record_and_save_audio.py
import sounddevice as sd
import wave
import os
import threading

def record_audio(filename, duration, samplerate):
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()

    # Save audio as WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved as {filename}")

def record_and_save_audio(filename, duration=5, samplerate=44100):
    record_audio(filename, duration, samplerate)

if __name__ == "__main__":
    # Set the filename for the WAV file
    filename = os.path.join("static", "recorded_audio.wav")

    # Create the code folder if it doesn't exist
    static_folder = "static"
    os.makedirs(static_folder, exist_ok=True)

    # Record and save audio
    record_and_save_audio(filename)
