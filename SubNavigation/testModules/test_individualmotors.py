from gpiozero import Motor
import time

# Define GPIO pins
FORWARD_5, REVERSE_5 = 4, 17
FORWARD_6, REVERSE_6 = 13, 26
FORWARD_3, REVERSE_3 = 5, 6
FORWARD_4, REVERSE_4 = 12, 16
FORWARD_1, REVERSE_1 = 27, 22
FORWARD_2, REVERSE_2 = 23, 24

# Motors dictionary
motors = {
    "motorE": Motor(FORWARD_1, REVERSE_1),
    "motorF": Motor(FORWARD_2, REVERSE_2),
    "motorD": Motor(FORWARD_3, REVERSE_3),
    "motorC": Motor(FORWARD_4, REVERSE_4),
    "motorA": Motor(FORWARD_5, REVERSE_5),
    "motorB": Motor(FORWARD_6, REVERSE_6)
}

if __name__ == "__main__":
    print("Starting Motor Test")
    speed = 0.5  # Speed is supported if using PWM; adjust logic otherwise

    for motor_name, motor in motors.items():
        print(f"Testing {motor_name}")
        motor.forward()  # Replace with motor.forward(speed) if using PWM
        time.sleep(2)
        motor.stop()
        time.sleep(1)

    print("Done Testing")
