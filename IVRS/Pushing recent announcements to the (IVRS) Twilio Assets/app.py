import os
from gtts import gTTS
from googletrans import Translator

def translate_and_save(text, target_lang, file_name):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    tts = gTTS(text=translation.text, lang=target_lang)
    
    # Create the 'static' directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    file_path = os.path.join('static', file_name)
    tts.save(file_path)
    return file_path

def main():
    user_input = input("Enter the text to translate: ")

    languages = {
        'marathi': 'mr',
        'english': 'en',
        'tamil': 'ta',
        'hindi': 'hi',
        'french': 'fr',
        'german': 'de'
    }

    for lang_name, lang_code in languages.items():
        file_name = f'{lang_name}_translation.mp3'
        file_path = translate_and_save(user_input, lang_code, file_name)
        print(f'Translation to {lang_name}: {file_path}')

if __name__ == "__main__":
    main()
