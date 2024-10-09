'''from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file:
        filepath = os.path.join('/app/data', file.filename)
        file.save(filepath)
        # Assume you have a function to handle transcription
        result = transcribe(filepath)  # Function you would define to use Whisper or similar
        return jsonify(result)
    return jsonify({'error': 'No file provided'}), 400

def transcribe(file_path):
    # Placeholder for your transcription logic
    return {"transcription": "transcribed text"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
import subprocess
import record_voice
def run_docker_container():
    try:
        # Define the command to run your Docker container non-interactively
        command = [
            "docker", "run", "--rm",
            "--cpus=5", "--memory=6g",  # Adjust these values based on your system's capability
            "-v",
            "C:/Users/adamr/OneDrive/שולחן העבודה/project/pythonProject1/Final_Project/SharedData/audio:/app/data",
            "voice-detector-app"
        ]

        # Execute the Docker command with UTF-8 encoding
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', check=True)

        # Print the output from Docker
        if result.stdout:
            print("Output from Docker:")
            print(result.stdout)
            return result.stdout


    except subprocess.CalledProcessError as e:
        print(f"Docker command failed with exit status {e.returncode}")
        print(e.output)

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to run the Docker container
def main():
    return(run_docker_container())
