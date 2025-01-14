import cv2
import mediapipe
from math import sqrt


def landmarksDetection(image, results, draw=False):
    """Detects landmarks on the face and optionally draws them on the image."""
    image_height, image_width = image.shape[:2]
    mesh_coordinates = [
        (int(point.x * image_width), int(point.y * image_height))
        for point in results.multi_face_landmarks[0].landmark
    ]
    if draw:
        [cv2.circle(image, coord, 2, (0, 255, 0), -1) for coord in mesh_coordinates]
    return mesh_coordinates


def euclideanDistance(point, point1):
    """Calculates the Euclidean distance between two points."""
    x, y = point
    x1, y1 = point1
    return sqrt((x1 - x) ** 2 + (y1 - y) ** 2)


def blinkRatio(image, landmarks, right_indices, left_indices):
    """Calculates the blink ratio for both eyes."""
    # Right eye landmarks
    right_horizontal = euclideanDistance(landmarks[right_indices[0]], landmarks[right_indices[8]])
    right_vertical = euclideanDistance(landmarks[right_indices[12]], landmarks[right_indices[4]])

    # Left eye landmarks
    left_horizontal = euclideanDistance(landmarks[left_indices[0]], landmarks[left_indices[8]])
    left_vertical = euclideanDistance(landmarks[left_indices[12]], landmarks[left_indices[4]])

    # Eye ratios
    right_eye_ratio = right_horizontal / right_vertical
    left_eye_ratio = left_horizontal / left_vertical

    # Average eye ratio
    return (right_eye_ratio + left_eye_ratio) / 2


def start_liveness_detection():
    """Main function for detecting liveness by tracking eye blinks."""
    COUNTER = 0
    TOTAL_BLINKS = 0

    FONT = cv2.FONT_HERSHEY_SIMPLEX

    # Eye landmark indices
    LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
    RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

    # Initialize Mediapipe Face Mesh
    face_mesh = mediapipe.solutions.face_mesh.FaceMesh(
        max_num_faces=1, min_detection_confidence=0.6, min_tracking_confidence=0.7
    )
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize and process the frame
        frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # If face landmarks are detected
        if results.multi_face_landmarks:
            landmarks = landmarksDetection(frame, results, draw=True)

            # Calculate blink ratio
            eyes_ratio = blinkRatio(frame, landmarks, RIGHT_EYE, LEFT_EYE)

            # Display blink message
            cv2.putText(
                frame, "Please blink your eyes", (50, 100), FONT, 1, (0, 255, 0), 2
            )

            # Count blinks
            if eyes_ratio > 3:
                COUNTER += 1
            else:
                if COUNTER > 4:  # If eyes were closed for multiple frames
                    TOTAL_BLINKS += 1
                    COUNTER = 0

            # Display total blinks
            cv2.rectangle(frame, (20, 120), (290, 160), (0, 0, 0), -1)
            cv2.putText(
                frame, f"Total Blinks: {TOTAL_BLINKS}", (30, 150), FONT, 1, (0, 255, 0), 2
            )

        # Display the frame
        cv2.imshow("Liveness Detection", frame)
        if cv2.waitKey(2) & 0xFF == 27:  # Exit on pressing ESC
            break

    # Cleanup
    video_capture.release()
    cv2.destroyAllWindows()


# Run the liveness detection function
start_liveness_detection()
