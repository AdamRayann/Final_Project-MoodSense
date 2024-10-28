import whisper
import os
import llama

def whisper_it(audio_path):
    try:
        # Check if the file exists
        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return None

        # Load the Whisper model
        model = whisper.load_model('base')

        # Transcribe the audio file
        result = model.transcribe(audio_path, fp16=False, language="en")
        transcript = result.get('text', '')

        if transcript:
            #print("Transcription:", transcript)
            return transcript
        else:
            print("No transcription available.")
            return None

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None

def analyze_with_llama(transcription):
    try:
        # Call the Llama analysis function and return its result
        return llama.main(transcription)
    except Exception as e:
        print(f"An error occurred during Llama analysis: {e}")
        return None

if __name__ == "__main__":
    # Specify the path to the audio file
    audio_file_path = "/app/data/output.mp3"

    # Transcribe the recorded audio using Whisper
    transcription = whisper_it(audio_file_path)

    if transcription:
        # Pass the transcription to the Llama model for analysis
        result = analyze_with_llama(transcription)

        if result:
            # Print the final Llama analysis result
            print(f"Detected Emotion: {result}")
