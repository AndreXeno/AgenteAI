import speech_recognition as sr

def record_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Parla pure, sto ascoltando...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="it-IT")
        print(f"🗣️ Hai detto: {text}")
        return text
    except sr.UnknownValueError:
        return "Non ho capito bene, puoi ripetere?"