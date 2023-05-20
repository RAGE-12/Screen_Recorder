import cv2
import pyautogui
import threading
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

# Define global variables
recording = False
output_file_prefix = 'recording'
output_file_extension = '.avi'
recording_number = 1

def start_recording():
    global recording, recording_number
    recording = True
    screen_size = pyautogui.size()  # Get the screen size dynamically
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_file = f'{output_file_prefix}{recording_number}{output_file_extension}'
    recording_number += 1
    out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)

    logo = cv2.imread('C:/Users/KIIT/OneDrive/Documents/pythonProject/screen recorder/logo.png', cv2.IMREAD_UNCHANGED)  # Load the logo image with alpha channel
    # specify desired width
    logo_width = 100
    logo_height = 100
    logo_resized = cv2.resize(logo, (logo_width, logo_height))  # Resize the logo to a desired size

    while recording:
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Define the region where the logo will be placed (e.g., top-right corner)
        x_offset = frame.shape[1] - logo_resized.shape[1] - 10
        y_offset = 10

        # Blend the logo with the frame using alpha channel
        alpha_s = logo_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            frame[y_offset:y_offset + logo_resized.shape[0], x_offset:x_offset + logo_resized.shape[1], c] = (
                    alpha_s * logo_resized[:, :, c] + alpha_l * frame[y_offset:y_offset + logo_resized.shape[0],
                                                                x_offset:x_offset + logo_resized.shape[1], c]
            )

        out.write(frame)

    out.release()


def stop_recording():
    global recording
    recording = False


def start_recording_thread():
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()


# Create a simple UI using Tkinter
root = tk.Tk()
root.title("Screen Recorder")

# Load the logo image using PIL
logo_image = Image.open('C:/Users/KIIT/OneDrive/Documents/pythonProject/screen recorder/logo.png')
logo_image = logo_image.resize((300, 300), Image.ANTIALIAS)
logo_tk = ImageTk.PhotoImage(logo_image)

# Create a label to display the logo
logo_label = tk.Label(root, image=logo_tk)
logo_label.pack(pady=10)

start_button = tk.Button(root, text="Start Recording", command=start_recording_thread)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state=tk.DISABLED)
stop_button.pack(pady=5)

def update_button_state():
    if recording:
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    else:
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

    root.after(100, update_button_state)

update_button_state()
root.mainloop()