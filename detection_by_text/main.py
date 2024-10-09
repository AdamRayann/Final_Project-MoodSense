# background_classifier.py

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
def run_classifier():
    classifier = TextClassifier()
    transcript=voice_detector_api.main()
    print(transcript)
    classifier.classify_text(transcript)





if __name__ == "__main__":
    thread = threading.Thread(target=run_classifier)
    thread.start()
