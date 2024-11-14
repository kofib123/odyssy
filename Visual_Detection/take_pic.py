from picamera2 import Picamera2, Preview
from time import sleep

# Initialize camera
picam2 = Picamera2()

# Configure and start the camera
config = picam2.create_still_configuration()
picam2.configure(config)


picam2.start()
num_pics =5
intervals = 2

print("starting")
for i in range(11,16):
    # Allow time for adjusting and viewing preview 

    # Capture image
    # Let the camera adjust to lighting
    image_path = f"/home/ODYSSY/important_code/Visual_Detection/captured_image{i+1}.jpg"
    picam2.capture_file(image_path)
    print(f"Image {i+1} saved at {image_path}")
    sleep(intervals)
picam2.stop()
print("Done")


