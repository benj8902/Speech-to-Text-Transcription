import pyaudio
import wave
import speech_recognition as sr
from tkinter import messagebox

# Initialize variables
RATE = 44100
CHUNK = 1024
RECORDING_TIME = 5
AUDIO_FORMAT = pyaudio.paInt16
OUTPUT_FILENAME = "recording.wav"
TRANSCRIPT_FILENAME = "transcript.txt"


# Function for recording audio
def record():
    print("Starting recording...")
    # Initialize audio input
    audio_input = pyaudio.PyAudio()

    # Set audio preferences
    stream_audio = audio_input.open(
        format=AUDIO_FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording in progress...")

    # Array for frames buffer
    frames = []

    # Adds chunks to frames buffer
    for _ in range(0, int(RATE / CHUNK * RECORDING_TIME)):
        data = stream_audio.read(CHUNK)
        frames.append(data)

    print("Recording finished. Transcription generating...")

    # Terminate input streaming
    audio_input.terminate()
    stream_audio.close()
    stream_audio.stop_stream()

    # Save audio to .wav file

    with wave.open(OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio_input.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"File saved as {OUTPUT_FILENAME}")
    return OUTPUT_FILENAME


# Function for transcription of the input audio
def transcribe(audio_filename, result_text):

    recognizer = sr.Recognizer()
    try:
        # Transcribe audio using Google transcription API
        with sr.AudioFile(audio_filename) as source:
            print("Transcribing audio...")
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)

            # Update UI
            result_text.delete(1.0, "end")
            print(transcription)
            result_text.insert("end", transcription)

            print("Transcription: " + transcription)

            # Save to txt file
            with open(TRANSCRIPT_FILENAME, "w") as f:
                f.write(transcription)
            messagebox.showinfo(f"Transcription", f"Transcription saved to {OUTPUT_FILENAME}")

    except sr.UnknownValueError:
        messagebox.showwarning("Error", "Google Speech Recognition could not understand the audio.")

    except sr.RequestError as e:
        messagebox.showwarning("Error", f"Could not request results from Google Speech Recognition service; {e}")





# if __name__ == "__main__":
#     record()  # Test recording directly

