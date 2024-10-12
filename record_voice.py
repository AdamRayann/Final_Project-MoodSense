import pyaudio
import wave
import threading
import os
import compress_wav  # Ensure this import is correct and available

class AudioRecorder:
    def __init__(self, filename="./SharedData/audio/output.wav", rate=16000):
        self.filename = filename
        self.rate = rate
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.frames = []
        self.recording = False
        self.stream = None
        self.audio_interface = pyaudio.PyAudio()

    def start_recording(self):
        """Start recording audio continuously until paused."""
        self.frames = []
        self.recording = True

        # Open the audio stream
        self.stream = self.audio_interface.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("Recording started...")
        threading.Thread(target=self.record).start()

    def record(self):
        """Continuously record audio in a background thread."""
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def pause_recording(self):
        """Pause the recording and save the audio."""
        if not self.recording:
            return

        print("Recording paused.")
        self.recording = False

        # Stop the audio stream
        self.stream.stop_stream()
        self.stream.close()

        # Save and compress the recorded audio
        self.save_audio()

    def save_audio(self):
        """Save recorded frames to a WAV file."""
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))

        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio_interface.get_sample_size(self.FORMAT))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Audio saved to {self.filename}")

        # Compress the saved audio
        try:
            print("Compressing audio...")
            compress_wav.main()  # Ensure this function is correctly implemented in the compress_wav module
            print("Audio compression complete.")
        except Exception as e:
            print(f"Error during audio compression: {e}")

    def terminate(self):
        """Terminate the PyAudio interface."""
        self.audio_interface.terminate()
