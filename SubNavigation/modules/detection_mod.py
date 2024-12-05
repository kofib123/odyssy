import cv2
from ultralytics import YOLO

def process_frame(frame, model, threshold=0.7):
    """
    Process a single frame for object detection.

    Args:
        frame (np.ndarray): The image frame to process.
        model (YOLO): The YOLO model for detection.
        threshold (float): Confidence threshold for detection.

    Returns:
        np.ndarray: The annotated frame.
        list: A list of detected objects with their centers.
    """
    screen_height, screen_width, _ = frame.shape
    screen_midpoint = (screen_width // 2, screen_height // 2)

    # Create a copy of the frame for annotations
    annotated_frame = frame.copy()

    # Draw screen center
    cv2.circle(annotated_frame, screen_midpoint, 5, (255, 0, 0), -1)
    cv2.putText(annotated_frame, "Screen Center", 
                (screen_midpoint[0] - 50, screen_midpoint[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Run YOLO detection
    results = model(frame)
    valid_boxes = [box for box in results[0].boxes if box.conf >= threshold]

    detected_objects = []
    for box in valid_boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        detected_objects.append(center)

        # Draw detections
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Testudo", (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(annotated_frame, center, 5, (0, 0, 255), -1)

    return annotated_frame, detected_objects
