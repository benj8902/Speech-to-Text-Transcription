import speech_recognition as sr
import threading

end_transcription = False
recognizer = None
microphone = None


def init_recognizer(result_text):
    global recognizer, microphone
    result_text.insert("end", "Finding microphone...\n")
    result_text.update_idletasks()

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        result_text.insert("end", "Ready to go!\n")
        result_text.update_idletasks()


def live_transcription(result_text):
    global end_transcription
    end_transcription = False

    def listen():
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            result_text.insert("end", "Listening...\n")
            print("Listening...")

            while not end_transcription:
                try:
                    input_audio = recognizer.listen(source, timeout=3)
                    transcription = recognizer.recognize_google(input_audio)
                    print(f"Transcription: {transcription}")
                    result_text.insert("end", transcription + "\n")
                    result_text.update_idletasks()
                except sr.UnknownValueError:
                    update_transcription(result_text, "Could not understand the audio.\n")
                except sr.RequestError as e:
                    update_transcription(result_text, f"API error: {e}. Ending live recording.\n")
                    break
                except Exception as e:
                    update_transcription(result_text, f"Error: {e}. Ending live recording.\n")
                    break

    threading.Thread(target=listen, daemon=True).start()  # Run listening in a separate thread


def update_transcription(result_text, message):
    result_text.insert("end", message + "\n")
    result_text.update_idletasks()


def end_live_transcription():
    global end_transcription
    end_transcription = True
