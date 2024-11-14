from picamera2 import Picamera2
from time import sleep

# Initialize camera
picam2 = Picamera2()

# Configure and start the camera
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

# Capture image
sleep(2)  # Let the camera adjust to lighting
image_path = "/home/pi/captured_image.jpg"
picam2.capture_file(image_path)
picam2.stop()

print(f"Image saved at {image_path}")

