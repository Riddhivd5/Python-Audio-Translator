from translate import Translator
from gtts import gTTS
import os
from customtkinter import *
import customtkinter as Ctk
from tkinter import *
from tkinter import messagebox

import tkinter as tk
import speech_recognition as sr

'''language_mapping = {
    "Hindi": "hi",
    "Marathi": "mr",
    "French": "fr",
    "Espanol": "es"
}'''

def start_translation():
    target_language = input_language.get()
    text_to_translate = tttrans.get("1.0", "end-1c")  # Get text from the Textbox

    if text_to_translate:
        translator = Translator(to_lang=target_language)
        translated_text = translator.translate(text_to_translate)

        # Update the GUI with translated text
        trans.delete("1.0", END)
        trans.insert(END, translated_text)

    else:
        print("No text to translate.")

def translate_text(text_to_translate, target_language):
    tts = gTTS(text=text_to_translate, lang=target_language)
    tts.save("translated_audio.mp3")

    print("Translated audio saved as 'translated_audio.mp3'")
    os.system("start translated_audio.mp3")



def open_speak_page():
    def start_audio_translation():
        target_language_2 = selected_language.get()
        r = sr.Recognizer()
        audio_path = r"C:\Users\Riddhi\Downloads\Untitled-video-Made-with-Clipchamp-_1_.wav"

        with sr.AudioFile(audio_path) as source:
            print("Listening...")
            try:
                audio_data = r.record(source)
                rec_text = r.recognize_google(audio_data)
            except sr.UnknownValueError:
                print("Could not understand audio.")
                rec_text = ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                rec_text = ""

        if rec_text:
            try:
                translator = Translator(to_lang=target_language_2)
                translated_text = translator.translate(rec_text)

                # Update the GUI with recognized text
                display_rec.delete("1.0", END)
                display_rec.insert(END, rec_text)

                # Update the GUI with translated text
                display.delete("1.0", END)
                display.insert(END, translated_text)

            except StopIteration:
                print("Translation failed due to StopIteration.")
        else:
            print("No text to translate.")



    def listen_text(rec_text, target_language_2):
        tts = gTTS(text=rec_text, lang=target_language_2)
        tts.save("translated_audio.mp3")
        os.system("start translated_audio.mp3")


    speak_page = CTk()
    speak_page.title("AudioMate - Speak Page")
    speak_page.geometry("400x700")

    
    selected_language = CTkOptionMenu(speak_page, values=["hi","mr","fr"], width=10)
    selected_language.pack(side=TOP)
    CTkLabel(speak_page, text="Enter Destination Language Code:", text_color="white", font=("", 15)).pack(side=TOP)

    speak_button = CTkButton(speak_page, text='Speak', font=("", 15), height=20, command=start_audio_translation)
    speak_button.pack(side=TOP, pady=50)

    listen_button = CTkButton(speak_page, text="Listen", font=("", 15), cursor="hand2", command=lambda: listen_text(display.get("1.0", "end-1c"), selected_language.get()))
    listen_button.pack(side=TOP, padx=0.5, pady=0.5)

    center_frame = CTkFrame(speak_page)
    center_frame.pack(expand=False, fill=BOTH)


    CTkLabel(center_frame, text="Recognized text", font=("", 15)).pack(pady=5)
    display_rec = CTkTextbox(center_frame)
    display_rec.pack(side=TOP)

    CTkLabel(center_frame, text="Translated text:", font=("", 15)).pack(pady=10)
    display = CTkTextbox(center_frame)
    display.pack(side=TOP)

    speak_page.mainloop()


Ctk.set_appearance_mode("System") 
Ctk.set_default_color_theme("blue") 

root = CTk()
root.title("AudioMate")
root.geometry("400x700")
root.config()

speak_label = CTkLabel(root, text="Want to speak instead?", text_color="white", font=("", 15, "bold"), height=40, width=60, cursor="hand2")
speak_label.pack(side=BOTTOM, padx=50, pady=30)
speak_label.bind("<Button-1>", lambda event: open_speak_page())

audio_label = CTkLabel(root, text="Want to upload a file instead?", text_color="white", font=("", 15, "bold"), height=40, width=60, cursor="hand2")
speak_label.pack(side=BOTTOM)

heading = CTkLabel(root, text="Let's Translate!", text_color="white", font=("", 25, "bold"))
heading.pack(side=TOP, padx=20, pady=40)

top_frame = CTkFrame(root, height=800, width=500, corner_radius=20)
top_frame.pack(padx=30, pady=80, expand=False, fill=BOTH)  # Set expand and fill options

CTkLabel(top_frame, text="Text to translate:", text_color="white", font=("", 15)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
CTkLabel(top_frame, text="Translated Text:", text_color="white", font=("", 15)).grid(row=2, column=0, padx=10, pady=5, sticky="w")

tttrans = CTkTextbox(top_frame, height=8)
tttrans.grid(row=1, column=0, padx=5, pady=5, sticky="w")

trans = CTkTextbox(top_frame, height=8)
trans.grid(row=3, column=0, padx=8, pady=10, sticky="w")

input_language = CTkOptionMenu(top_frame, values=["hi","mr","fr","zh","es"], width=10)
input_language.grid(row=5, column=0, padx=15, pady=5, sticky="w")
CTkLabel(top_frame, text="Enter Destination Language Code:", text_color="white", font=("", 15)).grid(row=4, column=0, padx=10, pady=5, sticky="w")

translate_button = CTkButton(root, text="Translate", font=("", 15), cursor="hand2", command=start_translation)
translate_button.pack(padx=0.5, pady=0.5, anchor=CENTER)

audio_button = CTkButton(root, text="Listen", font=("", 15), cursor="hand2", command=lambda: translate_text(trans.get("1.0", "end-1c"), input_language.get()))
audio_button.pack(side=TOP, padx=0.5, pady=0.5)

root.mainloop()
