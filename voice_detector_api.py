
import subprocess
import record_voice
def run_docker_container():
    try:

        # Define the command to run your Docker container
        command = [
            "docker", "run",
            "--cpus=5", "--memory=6g",  # Adjust these values based on your system's capability
            "-v",
            "C:/Users/adamr/OneDrive/שולחן העבודה/project/pythonProject1/Final_Project/SharedData/audio:/app/data",
            "voice-detector-app"
        ]

        # Execute the Docker command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', check=True)

        # Print the output from Docker
        if result.stdout:
            return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Docker command failed with exit status {e.returncode}")
        print(e.output)

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to run the Docker container
def main():
    return(run_docker_container())
