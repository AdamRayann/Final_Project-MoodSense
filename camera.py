import cv2
# camera.py
def start_camera():
    print("Camera has started.")

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections = face_detector.detectMultiScale(image_gray,minNeighbors=10)

        # Draw a rectangle around the faces
        for (x, y, w, h) in detections:
            #print(w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Camera has ended.")
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()