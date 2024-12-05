import cv2
import threading
import queue
from picamera2 import Picamera2
from ultralytics import YOLO

# =============================
# Initialization
# =============================
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

model = YOLO("/Users/ameenatafolabi/odyssy/Visual_Detection/Yellow_testudo/train1/best(2)")
model.fuse()

THRESHOLD = 0.7
FRAME_QUEUE = queue.Queue(maxsize=1)

# =============================
# Functions
# =============================
def process_frame(frame, result_queue):
    """
    Process a frame, perform object detection, and add results to the queue.
    """
    # screen_height, screen_width, _ = frame.shape
    # screen_midpoint = (screen_width // 2, screen_height // 2)
    results = model(frame)
    valid_boxes = [box for box in results[0].boxes if box.conf >= THRESHOLD]

    if valid_boxes:
        box = valid_boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2
        result_queue.put((x_center, y_center))  # Send detection data to the queue **

def capture_and_process(result_queue):
    """
    Continuously capture frames and process them for detection.
    """
    while True:
        frame = picam2.capture_array()
        process_frame(frame, result_queue)

def detect_code(result_queue):
    """
    Start detection in a separate thread or process.
    """
    capture_thread = threading.Thread(target=capture_and_process, args=(result_queue,), daemon=True)
    capture_thread.start()

def stop_camera():
    """
    Stop the camera safely.
    """
    picam2.stop()
    cv2.destroyAllWindows()
