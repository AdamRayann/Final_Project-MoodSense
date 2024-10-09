import numpy as np
import camera
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import emotions_classifier
import offline_classification
import cv2
from RoundButton import create_rounded_rectangle
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
import os
import glob
from datetime import datetime

model = emotions_classifier.load_model()

# GUI Class
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MoodSense")
        self.geometry("1200x700")
        self.configure(bg='#FFFFFF')  # Set background to white
        # Set the custom icon for the app window
        self.set_app_icon()

        # Load the background image path (not the actual image yet)
        self.bg_image_path = "entities/ios1.jpeg"
        self.bg_image = Image.open(self.bg_image_path)

        # Bind the window resize event to trigger the background resize function
        #self.bind('<Configure>', self.resize_background)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Create a custom style for the navigation bar
        self.style.configure('NavBar.TFrame', background='#3C73BE')
        self.style.configure('NavButton.TButton', font=('Helvetica', 14), padding=10, foreground='#FFFFFF',
                             background='#3C73BE')
        self.style.map('NavButton.TButton',
                       background=[('active', '#386AB0'), ('disabled', '#3C73BE')],  # Change color on hover
                       foreground=[('active', '#FFFFFF')])

        # Create the navigation bar
        self.create_navigation_bar()

        # Create frames for the content and sidebar
        content_container = ttk.Frame(self)
        content_container.pack(side='top', fill='both', expand=True)

        # Sidebar toggle state
        self.sidebar_open = False

        self.sidebar_frame = ttk.Frame(content_container, style='TFrame', relief=tk.RIDGE)
        self.sidebar_frame.pack(side='right', fill='y')
        self.sidebar_frame.pack_forget()  # Hide the sidebar initially

        self.content_frame = ttk.Frame(content_container, style='TFrame')
        self.content_frame.pack(side='left', fill='both', expand=True)

        # Create pages
        self.main_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.main_frame.pack(fill='both', expand=True)

        self.start_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.statistics_frame = ttk.Frame(self.content_frame, style='TFrame')

        self.page1_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.page2_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.history_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.share_frame = ttk.Frame(self.content_frame, style='TFrame')
        self.about_frame = ttk.Frame(self.content_frame, style='TFrame')

        # Create the sidebar
        self.create_sidebar()

        # Create main content pages
        self.create_main_page()
        self.create_start_page()
        self.create_page_image()
        self.create_share_page()
        self.creat_statistics_page()
        self.create_about_page()
        self.create_emotion_history()

        # Show the main page by default
        self.show_frame(self.start_frame)

    def set_app_icon(self):
        # Load the icon image (must be .ico or another image format)
        icon_image_path = "entities/app_icon.ico"  # Use .ico for best compatibility
        try:
            icon = Image.open(icon_image_path)
            icon = ImageTk.PhotoImage(icon)
            self.iconphoto(False, icon)  # Set the window icon
        except Exception as e:
            print(f"Error setting app icon: {e}")


    def create_sidebar(self):
        # Set the style for the sidebar frame, labels, and buttons
        self.style = ttk.Style()

        # Configure the style for the sidebar frame
        self.style.configure('Sidebar.TFrame', background='#3C73BE')

        # Configure the style for labels in the sidebar
        self.style.configure('Sidebar.TLabel', background='#3C73BE', foreground='white', font=('Helvetica', 20, 'bold'))

        # Configure the style for buttons in the sidebar
        self.style.configure('Sidebar.TButton', background='#3C73BE', foreground='white', padding=(10, 12))

        self.style.map('Sidebar.TButton',
                       background=[('active', '#386AB0')],  # Change the background color on hover
                       foreground=[('active', 'white')])  # Keep text color white on hover

        # Apply the custom background color to the sidebar frame
        self.sidebar_frame.config(style='Sidebar.TFrame')

        # Add an empty label as a spacer to lower the content
        self.spacer_label = ttk.Label(self.sidebar_frame, text="", style='Sidebar.TLabel')
        self.spacer_label.pack(pady=20, padx=60)  # Adjust padding to move content lower

        # Sidebar Title
        self.title_label = ttk.Label(self.sidebar_frame, text="MoodSense", style='Sidebar.TLabel')
        self.title_label.pack(pady=30)

        # Load and resize the icons (make sure you have valid icon paths)
        home_icon = Image.open("./entities/icons/home.png")
        home_icon = home_icon.resize((20, 20), Image.LANCZOS)
        home_icon = ImageTk.PhotoImage(home_icon)

        history_icon = Image.open("./entities/icons/history.png")
        history_icon = history_icon.resize((20, 20), Image.LANCZOS)
        history_icon = ImageTk.PhotoImage(history_icon)

        share_icon = Image.open("./entities/icons/share (1).png")
        share_icon = share_icon.resize((20, 20), Image.LANCZOS)
        share_icon = ImageTk.PhotoImage(share_icon)

        about_icon = Image.open("./entities/icons/about.png")
        about_icon = about_icon.resize((20, 20), Image.LANCZOS)
        about_icon = ImageTk.PhotoImage(about_icon)

        logout_icon = Image.open("./entities/icons/power.png")
        logout_icon = logout_icon.resize((20, 20), Image.LANCZOS)
        logout_icon = ImageTk.PhotoImage(logout_icon)

        # Sidebar buttons with icons
        self.nav_button1 = ttk.Button(self.sidebar_frame, text="Home", image=home_icon, compound='left', cursor="hand2",
                                      padding=(120, 12), style="Sidebar.TButton",
                                      command=lambda: self.show_frame(self.main_frame))
        self.nav_button1.image = home_icon  # Keep a reference to avoid garbage collection
        self.nav_button1.pack(pady=1)

        self.nav_button2 = ttk.Button(self.sidebar_frame, text="Emotion History", image=history_icon, compound='left',
                                      cursor="hand2", padding=(110, 12), style="Sidebar.TButton",
                                      command=lambda: self.show_frame(self.history_frame))
        self.nav_button2.image = history_icon  # Keep a reference
        self.nav_button2.pack(pady=1)

        self.nav_button3 = ttk.Button(self.sidebar_frame, text="Share", image=share_icon, compound='left',
                                      cursor="hand2", padding=(120, 12), style="Sidebar.TButton",
                                      command=lambda: self.show_frame(self.share_frame))

        self.nav_button3.image = share_icon  # Keep a reference
        self.nav_button3.pack(pady=1)

        self.nav_button4 = ttk.Button(self.sidebar_frame, text="About", image=about_icon, compound='left',
                                      cursor="hand2",
                                      padding=(120, 12), style="Sidebar.TButton",
                                      command=lambda: self.show_frame(self.about_frame))
        self.nav_button4.image = about_icon  # Keep a reference
        self.nav_button4.pack(pady=1)

        # Line separator
        self.line = ttk.Label(self.sidebar_frame, text="_________________", style='Sidebar.TLabel')
        self.line.pack(pady=50)

        self.nav_button5 = ttk.Button(self.sidebar_frame, text="Logout", image=logout_icon, compound='left',
                                      cursor="hand2", padding=(120, 12), style="Sidebar.TButton", command=self.quit)
        self.nav_button5.image = logout_icon  # Keep a reference
        self.nav_button5.pack(pady=10)

    def create_navigation_bar(self):
        # Create the navigation bar at the top
        nav_bar = ttk.Frame(self, style='NavBar.TFrame', height=50)
        nav_bar.pack(side='top', fill='x')

        # Load the logo image (replace with your image path)
        logo_image_path = "./entities/icons/logo.png"  # Add the correct path to your image
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((50, 40), Image.LANCZOS)  # Resize the image to fit in the navbar
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Add the image to the top left of the nav bar
        logo_label = tk.Label(nav_bar, image=logo_photo, background='#3C73BE')  # Set the same background color
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack(side='left', padx=20, pady=0)

        # Add the sidebar toggle button on the right
        sidebar_button = ttk.Button(nav_bar, cursor="hand2", text="☰", padding=(10, 12), style="NavButton.TButton",
                                    command=self.toggle_sidebar)
        sidebar_button.pack(side='right', padx=0, pady=0)

        # Center buttons A, B, C, D
        button_frame = ttk.Frame(nav_bar, style='NavBar.TFrame')
        button_frame.pack(side='top')

        self.style.configure('NavButton.TButton',
                             font=('Helvetica', 14),
                             padding=10,
                             foreground='#FFFFFF',
                             background='#3C73BE',
                             borderwidth=0,  # Remove the border
                             relief='flat')  # Make the button flat without borders

        button_a = ttk.Button(button_frame, padding=(10, 12), text="Live Detector", cursor="hand2",
                              style="NavButton.TButton", command=lambda: self.open_camera())
        button_a.pack(side='left', pady=0)

        button_b = ttk.Button(button_frame, padding=(10, 12), text="Attach Image", cursor="hand2",
                              style="NavButton.TButton", command=lambda: self.show_frame(self.page1_frame))
        button_b.pack(side='left', pady=0)

        button_c = ttk.Button(button_frame, padding=(10, 12), text="Statistics", cursor="hand2",
                              style="NavButton.TButton",
                              command=lambda: [self.creat_statistics_page(), self.show_frame(self.statistics_frame)])
        button_c.pack(side='left', pady=0)

        button_d = ttk.Button(button_frame, padding=(10, 12), text="History", cursor="hand2",
                              style="NavButton.TButton", command=lambda: self.show_frame(self.history_frame))
        button_d.pack(side='left', pady=0)

    def toggle_sidebar(self):
        # Function to open/close the sidebar
        if self.sidebar_open:
            self.sidebar_frame.pack_forget()  # Hide the sidebar
            self.sidebar_open = False
        else:
            self.sidebar_frame.pack(side='right', fill='y')  # Show the sidebar on the right
            self.sidebar_open = True

    def resize_background(self, frame, bg_label):
        # Get the current window size for the frame
        window_width = frame.winfo_width()
        window_height = frame.winfo_height()

        # Resize the background image to fit the current window size
        resized_bg_image = self.main_bg_image.resize((window_width, window_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_bg_image)

        # Update the background label with the resized image
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection

    def create_main_page(self):
        # Load background image for the main frame locally
        bg_image_path = "entities/ios1.jpeg"  # Path to your background image file

        # Open the background image using PIL and resize it to fit the main_frame
        self.main_bg_image = Image.open(bg_image_path)
        window_width = self.main_frame.winfo_width()
        window_height = self.main_frame.winfo_height()
        self.main_resized_bg_image = self.main_bg_image.resize((window_width, window_height), Image.LANCZOS)

        # Convert the resized image to a format that Tkinter can use
        self.main_bg_photo = ImageTk.PhotoImage(self.main_resized_bg_image)

        # Create a label to hold the background image in the main_frame
        if hasattr(self, 'main_bg_label'):
            self.main_bg_label.config(image=self.main_bg_photo)
            self.main_bg_label.image = self.main_bg_photo  # Keep reference to avoid garbage collection
        else:
            self.main_bg_label = tk.Label(self.main_frame, image=self.main_bg_photo)
            self.main_bg_label.image = self.main_bg_photo  # Keep reference to avoid garbage collection
            self.main_bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Create a Canvas to simulate a rounded square frame (div-like container)
        rounded_square_frame = tk.Canvas(self.main_frame, width=710, height=460, bg='#FFFFFF', highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 700, 450, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the GIF and buttons (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=670, height=420)  # Place it within the rounded square

        # Load the GIF image
        gif_path = "entities/Mor.gif"  # Path to your GIF image file
        self.gif = Image.open(gif_path)
        self.gif_width, self.gif_height = 450, 250  # Example size for GIF, adjust as needed

        # Create a label to hold the GIF inside the content frame
        self.gif_label = tk.Label(content_frame, borderwidth=0, bg='#D8E4FE')  # Match background color
        self.gif_label.pack(pady=10, padx=20)  # Add padding to space it inside the frame

        # Initialize frame index for GIF animation
        self.frame_index = 60

        # Start the GIF animation
        self.animate_gif()

        # Create the "Live Emotion Detector" button
        live_detector_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                         highlightthickness=0)
        live_detector_button.pack(pady=5)  # Add padding below the GIF inside the content frame

        # Draw a rounded rectangle as the button background using the imported function
        create_rounded_rectangle(live_detector_button, 10, 10, 230, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for "Live Emotion Detector"
        live_detector_button.create_text(120, 30, text="Live Emotion Detector", fill="white",
                                         font=('Helvetica', 14, 'bold'))

        # Bind the button click event for live emotion detection
        live_detector_button.bind("<Button-1>", lambda event: self.open_camera())

        # Create the "Attach Image to Detect Emotion" button
        attach_image_button = tk.Canvas(content_frame, cursor="hand2", width=200, height=60, bg='#D8E4FE', bd=0,
                                        highlightthickness=0)
        attach_image_button.pack(pady=10)  # Add padding below the GIF inside the content frame

        # Draw a rounded rectangle as the button background using the imported function
        create_rounded_rectangle(attach_image_button, 10, 10, 190, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for "Attach Image to Detect Emotion"
        attach_image_button.create_text(100, 30, text="Attach Image", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for attaching an image
        attach_image_button.bind("<Button-1>", lambda event: self.show_frame(self.page1_frame))

        # Resize event binding for dynamic background resizing
        self.main_frame.bind('<Configure>', self.resize_main_background)


    def resize_main_background(self, event):
        # Get the current window size for the main_frame
        window_width = self.main_frame.winfo_width()
        window_height = self.main_frame.winfo_height()

        # Resize the background image to fit the current window size
        self.main_resized_bg_image = self.main_bg_image.resize((window_width, window_height), Image.LANCZOS)
        self.main_bg_photo = ImageTk.PhotoImage(self.main_resized_bg_image)

        # Update the background label with the resized image
        self.main_bg_label.config(image=self.main_bg_photo)
        self.main_bg_label.image = self.main_bg_photo  # Keep reference to avoid garbage collection

    def create_start_page(self):
        # Load background image path for the start frame
        self.bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
        self.main_bg_image = Image.open(self.bg_image_path)

        # Create the background label for the start frame
        self.start_bg_label = tk.Label(self.start_frame)
        self.start_bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Bind the <Configure> event to dynamically resize the background
        self.start_frame.bind("<Configure>",
                              lambda event: self.resize_background(self.start_frame, self.start_bg_label))

        # Create a Canvas to simulate a rounded square frame (div-like container)
        rounded_square_frame = tk.Canvas(self.start_frame, width=710, height=460, bg='#FFFFFF', highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 700, 450, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the GIF and button (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=670, height=420)  # Place it within the rounded square

        # Load the GIF image
        gif_path = "entities/Mor.gif"  # Path to your GIF image file
        self.gif = Image.open(gif_path)
        self.gif_width, self.gif_height = 450, 250  # Example size for GIF, adjust as needed

        # Create a label to hold the GIF inside the content frame
        self.gif_label = tk.Label(content_frame, borderwidth=0, bg='#D8E4FE')  # Match background color
        self.gif_label.pack(pady=20, padx=20)  # Add padding to space it inside the frame

        # Initialize frame index for GIF animation
        self.frame_index = 0

        # Start the GIF animation
        self.animate_gif()

        # Create a custom rounded button using Canvas inside the content frame
        rounded_button = tk.Canvas(content_frame,cursor="hand2", width=200, height=60, bg='#D8E4FE', bd=0, highlightthickness=0)
        rounded_button.pack(pady=20)  # Add padding below the GIF inside the content frame

        # Draw a rounded rectangle as the button background using the imported function
        create_rounded_rectangle(rounded_button, 10, 10, 190, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text in the center
        rounded_button.create_text(100, 30, text="Let's Get Started!", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event
        rounded_button.bind("<Button-1>", lambda event: self.show_frame(self.main_frame))

    def create_page_image(self):
        # Load background image path for the page1 frame
        self.bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
        self.main_bg_image = Image.open(self.bg_image_path)

        # Create the background label for the page1 frame
        self.page1_bg_label = tk.Label(self.page1_frame)
        self.page1_bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Bind the <Configure> event to dynamically resize the background
        self.page1_frame.bind("<Configure>",
                              lambda event: self.resize_background(self.page1_frame, self.page1_bg_label))

        # Create a Canvas to simulate a rounded square frame (background)
        rounded_square_frame = tk.Canvas(self.page1_frame, width=710, height=460, bg='#FFFFFF', highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 700, 450, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the buttons and label (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=670, height=420)  # Place it within the rounded square

        # Create a custom rounded button for attaching an image
        attach_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                  highlightthickness=0)
        attach_button.pack(pady=20)  # Add padding to the button

        # Draw a rounded rectangle for the Attach Image button
        create_rounded_rectangle(attach_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Attach Image
        attach_button.create_text(120, 30, text="Attach Image", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for attaching an image
        attach_button.bind("<Button-1>", lambda event: self.attach_image())

        # Create a custom rounded button for returning to the main page
        return_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                  highlightthickness=0)
        return_button.pack(side='bottom', pady=20)  # Add padding to the button

        # Draw a rounded rectangle for the Return button
        create_rounded_rectangle(return_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Return to Main Page
        return_button.create_text(120, 30, text="Return to Main Page", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for returning to the main page
        return_button.bind("<Button-1>", lambda event: self.show_frame(self.main_frame))

        # Label to display the selected image inside the content frame
        self.image_label = ttk.Label(content_frame, background="#D8E4FE")
        self.image_label.pack(pady=10)

    def attach_image(self):
        # Allow user to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])

        # Check if a valid file path was returned
        if file_path:
            self.display_image(file_path)

    def animate_gif(self):
        # Get the next frame of the GIF
        try:
            self.gif.seek(self.frame_index)

            # Resize the current frame of the GIF
            resized_frame = self.gif.resize((self.gif_width, self.gif_height), Image.LANCZOS)
            gif_frame = ImageTk.PhotoImage(resized_frame)

            # Update the label with the resized frame
            self.gif_label.config(image=gif_frame)
            self.gif_label.image = gif_frame  # Keep a reference to avoid garbage collection

            # Move to the next frame, looping back to the beginning
            self.frame_index = (self.frame_index + 1) % self.gif.n_frames

            # Schedule the next frame update (adjust the delay as needed, e.g., 100ms)
            self.after(22, self.animate_gif)

        except Exception as e:
            print(f"Error animating GIF: {e}")

    def creat_statistics_page(self):
        # Clear existing content in the statistics_frame to avoid duplication
        for widget in self.statistics_frame.winfo_children():
            widget.destroy()

        # Load the initial background image and set up dynamic resizing
        self.bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
        self.main_bg_image = Image.open(self.bg_image_path)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.statistics_frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Bind the resize event to dynamically resize the background image using the shared function
        self.statistics_frame.bind("<Configure>",
                                   lambda event: self.resize_background(self.statistics_frame, self.bg_label))

        # Create a Canvas to simulate a rounded square frame (background)
        rounded_square_frame = tk.Canvas(self.statistics_frame, width=820, height=620, bg='#FFFFFF',
                                         highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 810, 610, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the statistics content (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=780, height=530)  # Place it within the rounded square

        # Find the most recent PNG file in the 'summary' directory
        summary_directory = 'summary'  # Directory where the images are saved
        list_of_files = glob.glob(os.path.join(summary_directory, '*.png'))  # Get all png files in the directory

        if list_of_files:
            most_recent_file = max(list_of_files, key=os.path.getctime)  # Get the most recent file by creation time
            try:
                # Load the most recent image
                image = Image.open(most_recent_file)
                image = image.resize((780, 450), Image.LANCZOS)  # Resize to fit within the frame
                image_photo = ImageTk.PhotoImage(image)

                # Display the image
                image_label = tk.Label(content_frame, image=image_photo, bg='#D8E4FE')
                image_label.image = image_photo  # Keep a reference to avoid garbage collection
                image_label.pack(pady=0)

            except Exception as e:
                error_label = ttk.Label(content_frame, text=f"Error loading image: {e}", background="#D8E4FE")
                error_label.pack(pady=10)
        else:
            # If no images found, show a message
            no_image_label = ttk.Label(content_frame, text="No summary images available", background="#D8E4FE")
            no_image_label.pack(pady=20)

        # Create a button to return to the main page
        return_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                  highlightthickness=0)
        return_button.pack(side='bottom', pady=0)

        # Draw a rounded rectangle for the Return button
        create_rounded_rectangle(return_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Return to Main Page
        return_button.create_text(120, 30, text="Return to Main Page", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for returning to the main page
        return_button.bind("<Button-1>", lambda event: self.show_frame(self.main_frame))

    def create_share_page(self):
        # Load background image path for the share frame
        self.bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
        self.main_bg_image = Image.open(self.bg_image_path)

        # Create the background label for the share frame
        self.share_bg_label = tk.Label(self.share_frame)
        self.share_bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Bind the <Configure> event to dynamically resize the background
        self.share_frame.bind("<Configure>",
                              lambda event: self.resize_background(self.share_frame, self.share_bg_label))

        # Create a Canvas to simulate a rounded square frame (background)
        rounded_square_frame = tk.Canvas(self.share_frame, width=710, height=460, bg='#FFFFFF', highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 700, 450, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the share options (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=670, height=420)  # Place it within the rounded square

        # Add a title for the share page
        title = ttk.Label(content_frame, text="Share Your Results", font=('Helvetica', 20, 'bold'),
                          background="#D8E4FE")
        title.pack(pady=10)

        # Social media sharing options (Icons + Labels)
        social_frame = tk.Frame(content_frame, bg='#D8E4FE')
        social_frame.pack(pady=20)

        # Load and resize social media icons
        fb_icon = Image.open("./entities/icons/facebook.png")
        fb_icon = fb_icon.resize((40, 40), Image.LANCZOS)
        fb_photo = ImageTk.PhotoImage(fb_icon)

        twitter_icon = Image.open("./entities/icons/twitter.png")
        twitter_icon = twitter_icon.resize((40, 40), Image.LANCZOS)
        twitter_photo = ImageTk.PhotoImage(twitter_icon)

        insta_icon = Image.open("./entities/icons/camera.png")
        insta_icon = insta_icon.resize((40, 40), Image.LANCZOS)
        insta_photo = ImageTk.PhotoImage(insta_icon)

        # Create a frame for each social media option
        def create_social_button(frame, icon, text):
            social_button_frame = tk.Frame(frame, bg='#D8E4FE')  # Create a frame to stack icon and label
            social_button_frame.pack(side='left', padx=30)

            # Icon (image on top)
            button = tk.Label(social_button_frame, image=icon, bg='#D8E4FE', cursor="hand2")
            button.image = icon  # Keep reference to avoid garbage collection
            button.pack()

            # Text (label below the icon)
            label = ttk.Label(social_button_frame, text=text, background="#D8E4FE", font=('Helvetica', 10, 'bold'))
            label.pack()

        # Add icons and their labels
        create_social_button(social_frame, fb_photo, "Facebook")
        create_social_button(social_frame, twitter_photo, "Twitter")
        create_social_button(social_frame, insta_photo, "Instagram")

        # Create a custom rounded button for downloading results
        download_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                    highlightthickness=0)
        download_button.pack(pady=20)  # Add padding to the button

        # Draw a rounded rectangle for the Download button
        create_rounded_rectangle(download_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Download Results
        download_button.create_text(120, 30, text="Download Results", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for downloading the result
        download_button.bind("<Button-1>", lambda event: self.download_results())

        # Create a custom rounded button for copying a shareable link
        link_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                highlightthickness=0)
        link_button.pack(pady=10)

        # Draw a rounded rectangle for the Copy Link button
        create_rounded_rectangle(link_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Copy Shareable Link
        link_button.create_text(120, 30, text="Copy Shareable Link", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for copying a link
        link_button.bind("<Button-1>", lambda event: self.copy_link_to_clipboard())


    def download_results(self):
        # Functionality to download results (to be implemented)
        print("Downloading results...")

    def copy_link_to_clipboard(self):
        # Functionality to copy shareable link (to be implemented)
        self.clipboard_clear()
        self.clipboard_append("https://www.moodsense.com/share")
        print("Copied shareable link to clipboard!")

    def create_about_page(self):
        # Load the initial background image and set up dynamic resizing
        self.bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
        self.main_bg_image = Image.open(self.bg_image_path)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.about_frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

        # Bind the resize event to dynamically resize the background image using the shared function
        self.about_frame.bind("<Configure>", lambda event: self.resize_background(self.about_frame, self.bg_label))

        # Create a Canvas to simulate a rounded square frame (background)
        rounded_square_frame = tk.Canvas(self.about_frame, width=820, height=825, bg='#FFFFFF', highlightthickness=0)
        rounded_square_frame.pack(pady=50, padx=50)

        # Draw a rounded rectangle as the background of the frame
        create_rounded_rectangle(rounded_square_frame, 10, 10, 810, 825, radius=50, fill="#D8E4FE", outline="#E0E0E0")

        # Create a frame inside the Canvas to hold the about content (in the rounded square)
        content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
        content_frame.place(x=20, y=20, width=780, height=830)  # Place it within the rounded square

        # Title for About Page
        title = ttk.Label(content_frame, text="About MoodSense", font=('Helvetica', 28, 'bold'), background="#D8E4FE")
        title.pack(pady=20)

        # Description of the app
        description = ttk.Label(content_frame, text=(
            "MoodSense is an innovative emotion recognition app that uses state-of-the-art machine learning algorithms "
            "to detect and analyze emotions in real-time. Whether you're analyzing your emotions through images or live detection, "
            "MoodSense offers a seamless experience with a sleek design and accurate results."
        ), wraplength=700, background="#D8E4FE", font=('Helvetica', 14), justify='center')
        description.pack(pady=10)

        # Fun fact or quote
        fun_fact = ttk.Label(content_frame, text=(
            '"The only real valuable thing is intuition." - Albert Einstein'
        ), background="#D8E4FE", font=('Helvetica', 16, 'italic'))
        fun_fact.pack(pady=15)

        # Add team member section
        team_label = ttk.Label(content_frame, text="Meet Our Team", font=('Helvetica', 20, 'bold'),
                               background="#D8E4FE")
        team_label.pack(pady=10)

        # Team members frame
        team_frame = tk.Frame(content_frame, bg='#D8E4FE')
        team_frame.pack(pady=10)

        # Add mock team members with images and roles
        team_members = [
            ("Adam Rayan", "./entities/icons/adam.png"),
            ("Majd Abbas", "./entities/icons/majd.png")
        ]

        for name, icon_path in team_members:
            # Load and display the team member image
            team_icon = Image.open(icon_path)
            team_icon = team_icon.resize((80, 80), Image.LANCZOS)
            team_photo = ImageTk.PhotoImage(team_icon)

            team_member_frame = tk.Frame(team_frame, bg='#D8E4FE')
            team_member_frame.pack(side='left', padx=30, pady=10)

            team_image_label = tk.Label(team_member_frame, image=team_photo, bg='#D8E4FE')
            team_image_label.image = team_photo  # Keep a reference to avoid garbage collection
            team_image_label.pack(pady=5)

            # Name and role of the team member
            name_label = tk.Label(team_member_frame, text=name, font=('Helvetica', 14, 'bold'), bg='#D8E4FE')
            name_label.pack()


        # Create a fun interactive button
        fun_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                               highlightthickness=0)
        fun_button.pack(pady=20)

        # Draw a rounded rectangle for the button
        create_rounded_rectangle(fun_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Return to Main Page
        fun_button.create_text(120, 30, text="Did You Know?", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event to display a fun fact
        fun_button.bind("<Button-1>", lambda event: self.display_fun_fact())

        # Create a button to return to the main page
        return_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                  highlightthickness=0)
        return_button.pack(pady=20)

        # Draw a rounded rectangle for the Return button
        create_rounded_rectangle(return_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

        # Add button text for Return to Main Page
        return_button.create_text(120, 30, text="Return to Main Page", fill="white", font=('Helvetica', 14, 'bold'))

        # Bind the button click event for returning to the main page
        return_button.bind("<Button-1>", lambda event: self.show_frame(self.main_frame))

    def display_fun_fact(self):
        # Display a fun fact in a new window
        fun_fact_window = tk.Toplevel(self)
        fun_fact_window.title("Did You Know?")
        fun_fact_window.geometry("400x200")

        fact_label = ttk.Label(fun_fact_window, text=(
            "Did you know?\nMoodSense uses over 10,000 images for training to identify emotions with accuracy!"
        ), wraplength=350, font=('Helvetica', 16), justify='center')
        fact_label.pack(pady=30)

    def display_image(self, file_path):
        # Ensure the file path is absolute
        file_path = os.path.abspath(file_path)

        # Check if the file exists before proceeding
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        # Try loading the image
        try:
            with open(file_path, 'rb') as f:
                file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # If OpenCV fails to load the image
            if image is None:
                print(f"Failed to load the image. Check file path or file integrity: {file_path}")
                return

            # Desired output size
            target_width, target_height = 250, 200

            # Get current image size
            h, w = image.shape[:2]

            # Resize the image while maintaining aspect ratio
            aspect_ratio = w / h
            if w > target_width or h > target_height:
                # Resize while keeping aspect ratio if the image is larger than the target
                if aspect_ratio > 1:  # Wider than tall
                    new_w = target_width
                    new_h = int(new_w / aspect_ratio)
                else:  # Taller than wide
                    new_h = target_height
                    new_w = int(new_h * aspect_ratio)
                image = cv2.resize(image, (new_w, new_h))
            else:
                # Keep original size if smaller
                new_w, new_h = w, h

            # Calculate padding to center the image
            pad_w = (target_width - new_w) // 2
            pad_h = (target_height - new_h) // 2

            # Add padding to the image to make it exactly 250x150
            image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT, value=[254, 228, 214])

            # Ensure the final image size is exactly 250x150 by slicing in case of rounding issues
            image = image[:target_height, :target_width]

            # Process the image (assuming offline_classification.main does some processing)
            image = offline_classification.main(model, image)

            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert the image to PIL format
            image_pil = Image.fromarray(image_rgb)

            # Convert the PIL image to a Tkinter image
            image_tk = ImageTk.PhotoImage(image_pil)

            # Display the image in a label
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

        except Exception as e:
            print(f"Error occurred while loading image: {e}")

    def create_emotion_history(self):
        def load_history():
            # Clear the previous content
            for widget in self.history_frame.winfo_children():
                widget.destroy()

            # Load background image for the emotion history frame
            bg_image_path = "entities/ios1.jpeg"  # Path to your background image file
            self.main_bg_image = Image.open(bg_image_path)

            # Create a label to hold the background image
            self.bg_label = tk.Label(self.history_frame)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make it cover the whole frame

            # Bind the resize event to dynamically resize the background image using the shared function
            self.history_frame.bind("<Configure>",
                                    lambda event: self.resize_background(self.history_frame, self.bg_label))

            # Create a Canvas to simulate a rounded square frame (background)
            rounded_square_frame = tk.Canvas(self.history_frame, width=820, height=620, bg='#FFFFFF',
                                             highlightthickness=0)
            rounded_square_frame.pack(pady=50, padx=50)

            # Draw a rounded rectangle as the background of the frame
            create_rounded_rectangle(rounded_square_frame, 10, 10, 810, 610, radius=50, fill="#D8E4FE",
                                     outline="#E0E0E0")

            # Create a frame inside the Canvas to hold the history content (in the rounded square)
            content_frame = tk.Frame(rounded_square_frame, bg='#D8E4FE')
            content_frame.place(x=20, y=20, width=780, height=530)  # Place it within the rounded square

            # Title for Emotion Detection History
            title = ttk.Label(content_frame, text="Emotion Detection History", font=('Helvetica', 24, 'bold'),
                              background='#D8E4FE')
            title.pack(pady=20)

            # Table Header
            table_header = tk.Frame(content_frame, bg='#D8E4FE')
            table_header.pack(fill='x', padx=10, pady=10)

            image_name_label = tk.Label(table_header, text="Image Name", bg="#D8E4FE", font=('Helvetica', 14, 'bold'))
            image_name_label.grid(row=0, column=0, padx=90, pady=5, sticky='w')

            time_label = tk.Label(table_header, text="Summary Time", bg="#D8E4FE", font=('Helvetica', 14, 'bold'))
            time_label.grid(row=0, column=1, padx=7, pady=5, sticky='w')

            action_label = tk.Label(table_header, text="Action", bg="#D8E4FE", font=('Helvetica', 14, 'bold'))
            action_label.grid(row=0, column=2, padx=80, pady=5, sticky='w')

            # Fetch the image history from the 'summary' directory
            summary_directory = 'summary'  # Directory where the images are saved
            list_of_images = glob.glob(os.path.join(summary_directory, '*.png'))  # Get all PNG files in the directory

            if list_of_images:
                # Table Body
                for index, image_path in enumerate(list_of_images):
                    image_name = os.path.basename(image_path)  # Get the file name (timestamp as image name)

                    # Extract time from the image name (assuming image name is timestamp)
                    try:
                        timestamp = os.path.splitext(image_name)[0]  # Remove file extension
                        summary_time = datetime.strptime(timestamp,
                                                         "%H%M%S")  # Assuming timestamp format like '20210922143015'
                        formatted_time = summary_time.strftime('%H:%M:%S')  # Format the time for display
                    except ValueError:
                        formatted_time = "Unknown"  # In case the image name isn't a valid timestamp

                    # Row frame
                    row_frame = tk.Frame(content_frame, bg='#D8E4FE')
                    row_frame.pack(fill='x', padx=50, pady=5)

                    # Image Name Column
                    image_label = tk.Label(row_frame, text=image_name, bg='#D8E4FE', font=('Helvetica', 12))
                    image_label.grid(row=index, column=0, padx=70, pady=5, sticky='w')

                    # Summary Time Column
                    time_label = tk.Label(row_frame, text=formatted_time, bg='#D8E4FE', font=('Helvetica', 12))
                    time_label.grid(row=index, column=1, padx=70, pady=5, sticky='w')

                    # Action (Clickable Label)
                    action_button = tk.Button(row_frame, text="View", font=('Helvetica', 12), bg='#3C73BE', fg='white',
                                              cursor="hand2",
                                              command=lambda path=image_path: self.show_image(path))
                    action_button.grid(row=index, column=2, padx=70, pady=5, sticky='w')
            else:
                # If no images found, show a message
                no_image_label = ttk.Label(content_frame, text="No summary images available", background="#D8E4FE")
                no_image_label.pack(pady=20)

            # Create a custom rounded button for returning to the main page
            return_button = tk.Canvas(content_frame, cursor="hand2", width=230, height=60, bg='#D8E4FE', bd=0,
                                      highlightthickness=0)
            return_button.pack(side='bottom', pady=20)

            # Draw a rounded rectangle for the Return button
            create_rounded_rectangle(return_button, 10, 10, 220, 50, radius=20, fill="#3C73BE", outline="#3C73BE")

            # Add button text for Return to Main Page
            return_button.create_text(120, 30, text="Return to Main Page", fill="white", font=('Helvetica', 14, 'bold'))

            # Bind the button click event for returning to the main page
            return_button.bind("<Button-1>", lambda event: self.show_frame(self.main_frame))

        # Reload the history page each time it's shown
        self.history_frame.bind("<Visibility>", lambda event: load_history())

    def show_image(self, image_path):
        # Create a new window to display the image
        image_window = tk.Toplevel(self)
        image_window.title("Image Summary")
        image_window.geometry("800x600")

        # Load and display the image
        image = Image.open(image_path)
        image = image.resize((780, 550), Image.LANCZOS)  # Resize to fit within the window
        image_photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(image_window, image=image_photo)
        image_label.image = image_photo  # Keep a reference to avoid garbage collection
        image_label.pack(fill='both', expand=True)

    def ask_camera_permission(self):
        # Create a new small window (dialog box)
        permission_window = tk.Toplevel(self)
        permission_window.title("Permission Required")
        permission_window.geometry("300x150")

        # Add a label asking for camera access permission
        label = ttk.Label(permission_window, text="Allow access to your camera?", font=('Helvetica', 12))
        label.pack(pady=20)

        # Create a frame for Yes and No buttons
        button_frame = ttk.Frame(permission_window)
        button_frame.pack(pady=10)

        # Yes button (grants permission and opens the camera)
        yes_button = ttk.Button(button_frame, text="Yes",
                                command=lambda: [permission_window.destroy(), camera.main(model)])
        yes_button.pack(side="left", padx=10)

        # No button (denies permission and closes the dialog)
        no_button = ttk.Button(button_frame, text="No", command=permission_window.destroy)
        no_button.pack(side="left", padx=10)

    def open_camera(self):
        self.ask_camera_permission()


    def show_frame(self, frame):
        # Hide all frames
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        frame.pack(fill='both', expand=True)

    def run(self):
        self.mainloop()


def main():
    app = GUI()
    app.run()


if __name__ == "__main__":
    main()
