import cv2
# camera.py
import time
import os
import cv2
import numpy as np

import emotions_classifier

def start_camera(model):
    print("Camera has started.")
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    video_capture = cv2.VideoCapture(0)
    frame_num=0
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture image")
            break

        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections = face_detector.detectMultiScale(image_gray, minNeighbors=10)

        # Draw a rectangle around the faces and return the face region
        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detected_face = frame[y:y + h, x:x + w]
            if frame_num % 5 ==0:
                # Return detected face
                #save_image_to_folder(detected_face,"detected_faces", str(frame_num)+".png")
                prediction = emotions_classifier.main(model,detected_face)
            frame_num+=1

            cv2.putText(frame, prediction,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0) ,2,cv2.LINE_AA)
            cv2.imshow('Detected Face', detected_face)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Sleep for 1 second before next capture
        #time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Camera has ended.")
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def save_image_to_folder(image, folder_name, image_name):
    # Ensure the image name has a valid extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    if not any(image_name.lower().endswith(ext) for ext in valid_extensions):
        raise ValueError(f"Image name must end with a valid extension: {valid_extensions}")

    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")

    # Create the full file path
    file_path = os.path.join(folder_name, image_name)

    # Save the image to the folder
    cv2.imwrite(file_path, image)
    print(f"Image saved at '{file_path}'.")


# Example usage
# Assuming 'image' is an image array loaded or captured by OpenCV, e.g., from a camera
# image = cv2.imread('your_image.jpg')  # Example of loading an image
# save_image_to_folder(image, 'saved_images', 'output_image.jpg')


def main():
    model=emotions_classifier.load_model()
    start_camera(model)