import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
from modules.detection_mod import process_frame

def test_detection(model_path: str, threshold: float = 0.7):
    """
    Test the detection functionality with live camera input.

    Args:
        model_path (str): Path to the YOLO model.
        threshold (float): Confidence threshold for detection.
    """
    # Initialize the camera
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Load the YOLO model
    model = YOLO(model_path)
    model.fuse()

    print("Starting detection test. Press 'q' to quit.")

    try:
        while True:
            # Capture a frame
            frame = picam2.capture_array()

            # Process the frame
            annotated_frame, detected_objects = process_frame(frame, model, threshold)

            # Print detected objects
            print(f"Detected Objects: {detected_objects}")

            # Display the annotated frame
            cv2.imshow("Detection Test", annotated_frame)

            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stopping detection test...")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        

if __name__ == "__main__":
    # Path to the trained YOLO model
    model_path = "/path/to/your/model"

    # Set the confidence threshold
    threshold = 0.7

    # Run the test
    test_detection(model_path, threshold)
