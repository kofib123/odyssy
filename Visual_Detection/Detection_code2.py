import cv2
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, List, Optional
import queue

@dataclass
class DetectionLabel:
    name: str
    color: Tuple[int, int, int]

class FrameProcessor:
    def __init__(self, model, threshold: float = 0.5):
        self.model = model
        self.threshold = threshold
        self.label_map = {
            0: DetectionLabel("Red Testudo", (0, 0, 255)),    # Red
            1: DetectionLabel("White Testudo", (255, 255, 255)), # White
            2: DetectionLabel("Yellow Testudo", (0, 255, 255))  # Yellow
        }
        
    def draw_screen_center(self, frame: np.ndarray) -> None:
        """Draw the screen center point and label."""
        height, width = frame.shape[:2]
        center = (width // 2, height // 2)
        cv2.circle(frame, center, 5, (255, 0, 0), -1)
        cv2.putText(frame, 
                   "Screen Center", 
                   (center[0] - 50, center[1] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, 
                   (255, 0, 0), 
                   2)

    def draw_detection(self, 
                      frame: np.ndarray, 
                      box: Tuple[int, int, int, int], 
                      label: DetectionLabel,
                      center: Tuple[int, int]) -> None:
        """Draw bounding box, label, and center point for a detection."""
        x1, y1, x2, y2 = box
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), label.color, 2)
        # Draw label text
        cv2.putText(frame, 
                   label.name, 
                   (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, 
                   label.color, 
                   2)
        # Draw center point
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
    def process_detections(self, 
                         frame: np.ndarray, 
                         detections: List) -> List[Tuple[str, Tuple[int, int]]]:
        """Process YOLO detections and return list of detected objects with their centers."""
        detected_objects = []
        
        for box in detections[0].boxes:
            if box.conf < self.threshold:
                continue
                
            # Get box coordinates and class
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            
            # Get label information
            label = self.label_map.get(
                class_id, 
                DetectionLabel("Unknown", (0, 255, 0))
            )
            
            # Calculate center
            center = ((x1 + x2) // 2, (y1 + y2) // 2)
            
            # Draw detection visualization
            self.draw_detection(
                frame, 
                (x1, y1, x2, y2), 
                label, 
                center
            )
            
            detected_objects.append((label.name, center))
            
        return detected_objects

    def process_frame(self, frame: np.ndarray, frame_queue: queue.Queue) -> None:
        """Process a single frame with object detection and visualization."""
        # Create a copy for annotations
        annotated_frame = frame.copy()
        
        # Draw screen center
        self.draw_screen_center(annotated_frame)
        
        # Run model and process detections
        results = self.model(frame)
        detected_objects = self.process_detections(annotated_frame, results)
        
        # Print detection information
        for name, center in detected_objects:
            print(f"{name} Bounding Box Center: {center}")
            
        # Update frame queue
        try:
            frame_queue.put(annotated_frame, block=False)
        except queue.Full:
            try:
                frame_queue.get_nowait()  # Discard old frame
                frame_queue.put(annotated_frame, block=False)
            except queue.Empty:
                pass
