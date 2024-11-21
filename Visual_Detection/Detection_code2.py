import cv2
import threading
import queue
from picamera2 import Picamera2
from ultralytics import YOLO

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Increased resolution for better detection
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load the YOLOv8 model
model = YOLO("/home/ODYSSY/important_code/Visual_Detection/best(2).pt")
model.fuse()

threshold = 0.7
frame_queue = queue.Queue(maxsize=1)  # Queue with maxsize=1 to always get the latest frame

# Define color mappings for different types of Testudos
color_map = {
    "red": (0, 0, 255),  # Red
    "white": (255, 255, 255),  # White
    "yellow": (0, 255, 255)  # Yellow
}

def process_frame(frame):
    # Calculate the screen's midpoint
    screen_height, screen_width, _ = frame.shape
    screen_midpoint = (screen_width // 2, screen_height // 2)

    # Create a new frame with filtered detections; Green: (0, 255, 0)
    annotated_frame = frame.copy()
    cv2.circle(annotated_frame, screen_midpoint, 5, (255, 0, 0), -1)  # Draw screen center in blue
    cv2.putText(annotated_frame, "Screen Center", (screen_midpoint[0] - 50, screen_midpoint[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Filter detections based on threshold (Processing YOLO detections)
    results = model(frame)
    valid_boxes = [box for box in results[0].boxes if box.conf >= threshold]

    for box in valid_boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = f"{box.cls[0]} {box.conf[0]:.2f}"

        # Assign a color based on the label/class
        color = (0, 255, 0)  # Default to green if class is unrecognized
        if box.cls[0] == "red":
            color = color_map["red"]
            label_text = "Red Testudo"
        elif box.cls[0] == "white":
            color = color_map["white"]
            label_text = "White Testudo"
        elif box.cls[0] == "yellow":
            color = color_map["yellow"]
            label_text = "Yellow Testudo"
        else:
            label_text = "Unknown Testudo"

        # Draw bounding box and label
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated_frame, label_text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Calculate the center of the bounding box
        x_center = (x1 + x2) // 2
        y_center = (y1 + y2) // 2
        cv2.circle(annotated_frame, (x_center, y_center), 5, (0, 0, 255), -1)  # Draw center point in red

        # Print the bounding box center
        print(f"{label_text} Bounding Box Center: ({x_center}, {y_center})")

    # Update the frame in the queue
    try:
        frame_queue.put(annotated_frame, block=False)
    except queue.Full:
        try:
            frame_queue.get_nowait()  # Discard the old frame
            frame_queue.put(annotated_frame, block=False)
        except queue.Empty:
            pass

def capture_and_process():
    while True:
        frame = picam2.capture_array()
        process_frame(frame)

# Start capturing and processing frames in a separate thread
capture_thread = threading.Thread(target=capture_and_process)
capture_thread.daemon = True
capture_thread.start()

# Main thread: Display the frames
try:
    while True:
        try:
            annotated_frame = frame_queue.get(timeout=1)
            cv2.imshow("Camera", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except queue.Empty:
            continue
finally:
    picam2.stop()
    cv2.destroyAllWindows()