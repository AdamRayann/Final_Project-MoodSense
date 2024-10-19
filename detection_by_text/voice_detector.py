import pyaudio
import wave
import whisper

# Initialize Whisper model (you can use 'base', 'small', 'medium', or 'large')
model = whisper.load_model("base")

# Record audio function
def record_audio(filename, duration=5, rate=16000):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()

    # Open the stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for _ in range(0, int(rate / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording complete")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the audio to a file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Transcribe audio using Whisper
def transcribe_audio(filename):
    print("Transcribing audio with Whisper...")
    result = model.transcribe(filename)
    print("Transcription: ", result["text"])


def whisper_it():
    model = whisper.load_model('base')
    res = model.transcribe('output.wav', fp16=False)
    print("Transcription:", res['text'])

if __name__ == "__main__":
    whisper_it()

'''    # Record audio for 5 seconds and save it as 'output.wav'
    audio_filename = "output.wav"
    record_audio(audio_filename, duration=5)

    # Transcribe the recorded audio
    transcribe_audio(audio_filename)'''