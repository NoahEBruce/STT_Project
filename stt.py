import tkinter as tk
from tkinter import filedialog 
from tkinter import simpledialog
import azure.cognitiveservices.speech as speechsdk

#Dialog box asking a user to select a language
def select_language():
    root = tk.Tk()
    root.withdraw()  

    selected_language = simpledialog.askstring("Language Selection", "Enter the language code (e.g., en-US, ja-JP):")
    return selected_language

#GUI asking user to select a WAC File
def get_file_path():
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(
        title="Select a WAV file",
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
    )

    return file_path

#Text Dump
def dump_to_file(text, file_path='recognized_text.txt'):
    with open(file_path, 'w') as file:
        file.write(text)
    print(f"Text written to {file_path}")

#Speech to Text 
def speech_to_text(subscription_key, region, language):
    audio_file_path = get_file_path()

    if not audio_file_path:
        print("No file selected. Exiting.")
        return

    print(f"Selected file: {audio_file_path}")
    
    try:

        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        speech_config.speech_recognition_language = language
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = result.text
            print("Recognized text: {}".format(recognized_text))
            dump_to_file(recognized_text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Run Section
subscription_key = "Enter your own Azure subscription Key"
region = "Enter your own region"
selected_language = select_language()
recognized_text = speech_to_text(subscription_key, region, selected_language)
