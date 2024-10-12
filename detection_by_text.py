# background_classifier.py
import queue

import joblib
import json
from transformers import pipeline
import numpy as np
import threading
import record_voice
import voice_detector_api



class TextClassifier:
    def __init__(self):
        self.labels = ["neutral", "positive", "negative", "surprise"]
        self.load_models()

    def convert_to_npns(self, arr):
        return [
            arr[4]['score'],
            arr[3]['score'],
            arr[0]['score'] + arr[1]['score'] + arr[2]['score'] + arr[5]['score'],
            arr[6]['score']
        ]

    def load_models(self):
        # Load models in the background
        with open("./text models/model_paths.json", "r") as json_file:
            model_paths = json.load(json_file)
        self.vectorizer = joblib.load(model_paths["vectorizer"])
        self.rf_classifier = joblib.load(model_paths["rf_classifier"])
        self.svm_model = joblib.load(model_paths["svm_classifier"])
        self.hartmann_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

    def classify_text(self, text):
        new_texts = [text]
        svm_predictions = np.array(self.svm_model.predict_proba(new_texts)[0])
        rf_predictions = np.array(self.rf_classifier.predict_proba(self.vectorizer.transform(new_texts))[0])
        hartmann_rf_predictions = self.hartmann_model(new_texts[0], return_all_scores=True)[0]
        hartmann_rf_predictions = np.array(self.convert_to_npns(hartmann_rf_predictions))

        preds = 0.22 * svm_predictions + 0.08 * rf_predictions + 0.7 * hartmann_rf_predictions
        print(self.labels[np.argmax(preds)])
        return self.labels[np.argmax(preds)]


# Function to run the classifier in a thread
# Assuming TextClassifier and voice_detector_api are implemented elsewhere
def run_classifier(result_queue):
    """Runs the classifier and puts the emotion in the result queue."""
    classifier = TextClassifier()
    transcript = voice_detector_api.main()

    # Classify the text and get the emotion
    emotion = classifier.classify_text(transcript)

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
    print(f"Detected Emotion: {emotion}")

    return emotion

