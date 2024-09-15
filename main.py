import numpy as np
import camera
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import emotions_classifier
import offline_classification
import cv2
import os
from tkinter import filedialog
from PIL import Image, ImageTk
model = emotions_classifier.load_model()

# GUI Class
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern GUI")
        self.geometry("600x600")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 14), padding=10)

        # face detector model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Create frames for each page
        self.main_frame = ttk.Frame(self)
        self.page1_frame = ttk.Frame(self)
        self.page2_frame = ttk.Frame(self)

        # Create all pages
        self.create_main_page()
        self.create_page_image()

        # Show the main page by default
        self.show_frame(self.main_frame)

    def create_main_page(self):
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(fill='both', expand=True)

        button1 = ttk.Button(self.main_frame, text="Attach image to detect emotion",
                             command=lambda: self.show_frame(self.page1_frame))
        button1.pack(pady=20)

        button2 = ttk.Button(self.main_frame, text="Live emotion detector",
                             command=self.open_camera)
        button2.pack(pady=20)

    def create_page_image(self):
        attach_button = ttk.Button(self.page1_frame, text="Attach Image", command=self.attach_image)
        attach_button.pack(pady=20)

        return_button = ttk.Button(self.page1_frame, text="Return to Main Page",
                                   command=lambda: self.show_frame(self.main_frame))
        return_button.pack(side='bottom', pady=20)

        self.image_label = ttk.Label(self.page1_frame)
        self.image_label.pack(pady=10)

    def attach_image(self):
        # Allow user to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])

        # Check if a valid file path was returned
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        # Ensure the file path is absolute
        file_path = os.path.abspath(file_path)

        # Check if the file exists before proceeding
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        # Try loading the image using the alternative method to handle Unicode paths
        try:
            with open(file_path, 'rb') as f:
                file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # If OpenCV fails to load the image, log an error
            if image is None:
                print(f"Failed to load the image. Check file path or file integrity: {file_path}")
                return

            # Resize the image while maintaining aspect ratio
            h, w = image.shape[:2]
            new_w, new_h = 400, int(400 * h / w)
            image = cv2.resize(image, (new_w, new_h))

            # Process the image using the offline classification function
            image = offline_classification.main(model, image)

            # Convert the image to RGB format (OpenCV uses BGR by default)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert the image from OpenCV format to PIL format
            image_pil = Image.fromarray(image_rgb)

            # Convert the PIL image to a format suitable for Tkinter display
            image_tk = ImageTk.PhotoImage(image_pil)

            # Display the image in a label (Tkinter GUI)
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

        except Exception as e:
            print(f"Error occurred while loading image: {e}")

    def open_camera(self):
        camera.main(model)

    def show_frame(self, frame):
        # Hide all frames
        for widget in self.winfo_children():
            widget.pack_forget()
        frame.pack(fill='both', expand=True)

    def run(self):
        self.mainloop()


def main():
    app = GUI()
    app.run()


if __name__ == "__main__":
    main()