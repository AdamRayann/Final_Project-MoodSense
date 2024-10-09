from pydub import AudioSegment


def compress_wav_to_mp3(wav_path, mp3_path, bitrate="192k"):
    """
    Compresses a WAV file to an MP3 file.

    Parameters:
    - wav_path: Path to the input WAV file.
    - mp3_path: Path to the output MP3 file.
    - bitrate: Bitrate for the output MP3 file.
    """
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_path)

    # Export as MP3
    audio.export(mp3_path, format="mp3", bitrate=bitrate)


def main():
    # Specify the path to your WAV file and the output MP3 file
    wav_file_path = "./SharedData/audio/output.wav"
    mp3_file_path = "./SharedData/audio/output.mp3"

    # Call the function
    compress_wav_to_mp3(wav_file_path, mp3_file_path)
