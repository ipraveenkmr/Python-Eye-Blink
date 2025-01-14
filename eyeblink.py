import cv2
import mediapipe
from math import sqrt
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import numpy as np
from ui import create_rounded_button


class EyeBlinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Blink Detector")
        self.root.geometry("800x600")
        self.recording = False
        self.face_mesh = mediapipe.solutions.face_mesh.FaceMesh(
            max_num_faces=1, min_detection_confidence=0.6, min_tracking_confidence=0.7
        )
        self.COUNTER = 0
        self.TOTAL_BLINKS = 0

        # Eye indices for Mediapipe Face Mesh
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

        # UI Components
        self.title_label = tk.Label(root, text="OpenCV Eye Blink Detection", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)
        
        self.record_button = ttk.Button(self.buttons_frame, text="Start", command=self.toggle_recording)
        # self.record_button = create_rounded_button(
        #     self.buttons_frame,
        #     text="Start",
        #     bg="#1e293b",
        #     command=self.toggle_recording,
        #     x=10, y=10,
        # )
        self.record_button.grid(row=0, column=0, padx=10)

        self.exit_button = ttk.Button(self.buttons_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=0, column=2, padx=10)

        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
        
        
    def toggle_recording(self):
        if not hasattr(self, "recording"):  # Ensure self.recording is initialized
            self.recording = False

        if self.recording:
            # Stop recording
            self.recording = False
            self.stop_recording()  # Call the stop logic
            self.record_button.config(text="Start")  # Update button text to "Start"
        else:
            # Start recording
            self.recording = True
            self.start_recording()  # Call the start logic
            self.record_button.config(text="Stop")  # Update button text to "Stop"

    def landmarks_detection(self, image, results):
        """Detect landmarks on the face."""
        image_height, image_width = image.shape[:2]
        return [
            (int(point.x * image_width), int(point.y * image_height))
            for point in results.multi_face_landmarks[0].landmark
        ]

    def euclidean_distance(self, point, point1):
        """Calculate Euclidean distance between two points."""
        return sqrt((point1[0] - point[0]) ** 2 + (point1[1] - point[1]) ** 2)

    def blink_ratio(self, landmarks, right_indices, left_indices):
        """Calculate blink ratio for both eyes."""
        right_horizontal = self.euclidean_distance(landmarks[right_indices[0]], landmarks[right_indices[8]])
        right_vertical = self.euclidean_distance(landmarks[right_indices[12]], landmarks[right_indices[4]])
        left_horizontal = self.euclidean_distance(landmarks[left_indices[0]], landmarks[left_indices[8]])
        left_vertical = self.euclidean_distance(landmarks[left_indices[12]], landmarks[left_indices[4]])
        return (right_horizontal / right_vertical + left_horizontal / left_vertical) / 2

    def update_frame(self):
        """Update video feed in the Tkinter window with liveness detection."""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                results = self.face_mesh.process(rgb_frame)

                if results.multi_face_landmarks:
                    landmarks = self.landmarks_detection(frame, results)
                    
                    for landmark in landmarks:
                        cv2.circle(frame, landmark, 1, (0, 255, 0), -1) 

                    # Calculate blink ratio
                    eyes_ratio = self.blink_ratio(landmarks, self.RIGHT_EYE, self.LEFT_EYE)

                    # Detect blink
                    if eyes_ratio > 3:
                        self.COUNTER += 1
                    else:
                        if self.COUNTER > 4:  # Eyes closed for multiple frames
                            self.TOTAL_BLINKS += 1
                            self.COUNTER = 0

                    # Draw blinks on the frame
                    cv2.putText(frame, f"Blinks: {self.TOTAL_BLINKS}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)

                # Convert to Tkinter-compatible format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                frame = cv2.resize(frame, (640, 480))
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_frame.config(image=img)
                self.video_frame.image = img

        if self.recording:
            self.root.after(10, self.update_frame)

    def start_recording(self):
        """Start video recording."""
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Camera not accessible!")
            return
        self.recording = True
        self.update_frame()

    def stop_recording(self):
        """Stop video recording."""
        self.recording = False
        blank_frame = np.full((480, 640, 3), 255, dtype=np.uint8)
        img = ImageTk.PhotoImage(Image.fromarray(blank_frame))
        self.video_frame.config(image=img)
        self.video_frame.image = img

    def exit_app(self):
        """Exit the application."""
        self.cap.release()
        self.root.destroy()



# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = EyeBlinkApp(root)
    root.mainloop()
