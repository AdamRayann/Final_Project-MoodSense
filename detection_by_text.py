# background_classifier.py
import queue

import joblib
import json
from transformers import pipeline
import numpy as np
import threading
import record_voice
import voice_detector_api






# Function to run the classifier in a thread
# Assuming TextClassifier and voice_detector_api are implemented elsewhere
def run_classifier(result_queue):
    """Runs the classifier and puts the emotion in the result queue."""

    transcript = voice_detector_api.main()

    # Classify the text and get the emotion
    emotion = transcript

    # Put the emotion into the queue
    result_queue.put(emotion)

def main():
    """Main function to start the classifier and print the emotion."""
    # Create a queue to communicate between threads
    result_queue = queue.Queue()

    # Start the classifier in a separate thread, passing the queue
    thread = threading.Thread(target=run_classifier, args=(result_queue,))
    thread.start()

    # Wait for the thread to complete and get the emotion from the queue
    thread.join()  # Ensure the thread finishes execution

    # Get the emotion result from the queue
    emotion = result_queue.get()

    # Print the emotion from the main function
    #print(f"Detected Emotion: {emotion}")

    return emotion

