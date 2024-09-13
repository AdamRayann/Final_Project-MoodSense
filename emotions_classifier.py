#%% Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,  Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from keras.models import save_model
from sklearn.metrics import accuracy_score, confusion_matrix
#import cnn_implementation


#%% loading the model
def load_model():
    with open('network_emotions.json', 'r') as json_file:
        json_saved_model=json_file.read()

    network_loaded=tf.keras.models.model_from_json(json_saved_model)
    print(json_saved_model)

    network_loaded.load_weights('weights_emotions.hdf5')
    network_loaded.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
    #network_loaded.summary()    # checks if the model was loaded as properly

    return network_loaded


def process_image(img):

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Uncomment if the model was trained on grayscale images
    img = cv2.resize(img, (48, 48))
    img = img / 255.0  # Ensure scaling is the same as during training
    roi = np.expand_dims(img, axis=0)
    return roi

def predict_emotion(model, image):
    processed_image=process_image(image)

    probs = model.predict(processed_image)

    predicted_emotion = np.argmax(probs)
    print(probs)
    return predicted_emotion


'''def process_image(image_path):
    img = cv2.imread(image_path)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Uncomment if the model was trained on grayscale images
    img = cv2.resize(img, (48, 48))
    img = img / 255.0  # Ensure scaling is the same as during training
    roi = np.expand_dims(img, axis=0)
    return roi'''

'''def predict_emotion(model, image_path):
    processed_image=process_image(image_path)

    probs = model.predict(processed_image)

    predicted_emotion = np.argmax(probs)
    print(probs)
    return predicted_emotion'''





def main(model,image):
    print("started..")
    emotions=["Angry","Disgusted","Fearful","Happy","Neutral","Sad","Surprised"]
    #model = load_model()
    #res=predict_emotion(model, image_path="./detected_faces/00.png")
    res=predict_emotion(model, image)
    print(emotions[res])
    return emotions[res]


