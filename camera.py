import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyautogui
import numpy as np

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter OpenCV Integration")
        self.root.geometry("800x600")
        self.recording = False

        # Create UI components
        self.title_label = tk.Label(root, text="OpenCV Demo", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        self.record_button = ttk.Button(self.buttons_frame, text="Record", command=self.start_recording)
        self.record_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(self.buttons_frame, text="Stop", command=self.stop_recording)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.screenshot_button = ttk.Button(self.buttons_frame, text="Screenshot", command=self.take_screenshot)
        self.screenshot_button.grid(row=0, column=2, padx=10)

        self.exit_button = ttk.Button(self.buttons_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=0, column=3, padx=10)

        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        """Continuously update the video feed in the Tkinter GUI."""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))  # Resize for consistent display
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_frame.config(image=img)
                self.video_frame.image = img
        if self.recording:
            self.root.after(10, self.update_frame)

    def start_recording(self):
        """Start recording the video feed."""
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Camera not accessible!")
            return
        self.recording = True
        self.update_frame()

    def stop_recording(self):
        """Stop recording the video feed."""
        self.recording = False
        blank_frame = np.full((480, 640, 3), 255, dtype=np.uint8)
        img = ImageTk.PhotoImage(Image.fromarray(blank_frame))
        self.video_frame.config(image=img)
        self.video_frame.image = img

    def take_screenshot(self):
        """Take a screenshot of the current screen."""
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        messagebox.showinfo("Screenshot", "Screenshot saved as screenshot.png")

    def exit_app(self):
        """Exit the application."""
        self.cap.release()
        self.root.destroy()


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
