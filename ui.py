import tkinter as tk
from transcription import record, transcribe
from realtime import live_transcription, end_live_transcription, init_recognizer
import threading


# Function to record and save the transcript to a .txt file
def complete_transcription():
    print("record button clicked")
    audio_filename = record()
    transcribe(audio_filename, result_text)


# Function calling for live_transcription from realtime.py
def transcribe_live():
    print("Transcribing as you speak...")
    live_transcription(result_text)
    # threading.Thread(target=live_transcription, args=(result_text,), daemon=True).start()


# Function calling end_live_transcription from realtime.py
def end_live_transcribe():
    print("Stopping live transcribing...")
    end_live_transcription()


# Function to generate GUI for transcription app
def create_ui():
    root = tk.Tk()
    root.title("Audio Transcriptor")
    root.geometry("500x300")

    global result_text
    result_text = tk.Text(root, height=8, width=50, wrap="word", font=("Ariel", 12))
    result_text.pack(pady=10)

    # Initialize recognizer and microphone in a separate thread during app startup
    threading.Thread(target=init_recognizer, args=(result_text,), daemon=True).start()

    label = tk.Label(root, text="Transcriptor App", font=("Arial", 16))
    label.pack(pady=10)

    # Define buttons and associated commands
    start_recording = tk.Button(root, text="Record", command=complete_transcription, font=("Ariel", 12),
                                cursor="hand1")
    start_recording.pack(pady=5)
    live_transcribe = tk.Button(root, text="Live Transcribe", command=transcribe_live, font=("Ariel", 12),
                                cursor="hand1")
    live_transcribe.pack(pady=5)
    stop_transcribe = tk.Button(root, text="Stop Transcription", command=end_live_transcribe, font=("Ariel", 12),
                                cursor="hand1")
    stop_transcribe.pack(pady=5)

    root.mainloop()

# if __name__ == "__main__":
#     create_ui()
