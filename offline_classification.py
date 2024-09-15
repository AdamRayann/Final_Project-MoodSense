import cv2
# camera.py
import time
import os
import cv2
import numpy as np

import emetions_summary
import emotions_classifier
import cv2


def offline_classify(model, image):
    print("Offline classification has started.")

    # Initialize the face detector
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Check if the image is valid
    if image is None:
        print("Failed to detect image. Image is None.")
        return

    # Convert the image to grayscale for face detection
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    detections = face_detector.detectMultiScale(image_gray, minNeighbors=10, minSize=(80, 80))

    # Check if any face is detected
    if len(detections) == 0:
        print("No faces detected.")
        return

    # Loop over all the detected faces
    for (x, y, w, h) in detections:
        # Draw a rectangle around the detected face in the original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the detected face region
        detected_face = image[y:y + h, x:x + w]

        # Prediction from the emotion classifier
        prediction = emotions_classifier.main(model, detected_face)

        # Display prediction summary
        emetions_summary.main(prediction)

        # Add text for prediction label above the detected face
        cv2.putText(image, prediction, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the result (show the entire image with rectangles and labels)
    cv2.imshow('Image', image)

    # Plot the emotion summary
    emetions_summary.plot_summary()
    return image
    # Wait for a key press and close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(model,image):
    res=offline_classify(model,image)
    return res

