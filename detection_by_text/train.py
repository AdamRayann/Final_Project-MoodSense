import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer
import openpyxl

from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.calibration import CalibratedClassifierCV

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import json
import joblib

print(openpyxl.__version__)


# Path to the Excel file
file_path = 'all_data_npns.xlsx'
df = pd.read_excel(file_path)
df['text'] = df['text'].astype(str)
df.dropna(subset=['text'], inplace=True)
texts = df['text'].values
y = np.array(df['label'].values)

# Tokenize the text
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
word_index = tokenizer.word_index

X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

linear_svc = LinearSVC()
calibrated_svc = CalibratedClassifierCV(linear_svc)
svm_model = make_pipeline(vectorizer, calibrated_svc)
svm_model.fit(X_train,y_train)

new_sentence = "This product exceeded my expectations!"
predicted_class = svm_model.predict([new_sentence])
predicted_proba = svm_model.predict_proba([new_sentence])
print(predicted_class)



rf_classifier = RandomForestClassifier(n_estimators=5, random_state=42)
rf_classifier.fit(X_train_tfidf, y_train)

y_pred = rf_classifier.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Optional: Print the classification report
print(classification_report(y_test,y_pred))



# Define file paths
rf_model_file = "text models/rf_classifier.joblib"
svm_model_file = "text models/svm_classifier.joblib"
vectorizer_file = "text models/tfidf_vectorizer.joblib"

joblib.dump(vectorizer , vectorizer_file)
joblib.dump(rf_classifier, rf_model_file)
joblib.dump(svm_model, svm_model_file)

# Create a dictionary to hold file paths
save_dict = {
    "vectorizer": vectorizer_file,
    "rf_classifier": rf_model_file,
    "svm_classifier": svm_model_file
}

# Save the dictionary to a JSON file
with open("text models/model_paths.json", "w") as json_file:
    json.dump(save_dict, json_file)

print("Models and vectorizer saved successfully.")
