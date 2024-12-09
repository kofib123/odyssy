from gpiozero import Motor
import RPi.GPIO as GPIO
import time

# Define GPIO pins
#FORWARD_5, REVERSE_5 = 4, 17
FORWARD_7, REVERSE_7 = 9,25
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
    "motorA": Motor(FORWARD_7, REVERSE_7),
    "motorB": Motor(FORWARD_6, REVERSE_6)
}

if __name__ == "__main__":
    try:
        print("Starting Motor Test")
        motor1 = motors["motorD"]
        motor2 = motors["motorC"]
        motor3 = motors["motorE"]
        motor4 = motors["motorF"]
        speed = 0.5  # Speed is supported if using PWM; adjust logic otherwise
        
        
        
        motor1.forward(0.8)
        motor2.forward(0.8)
        time.sleep(3)
        motor1.stop()
        motor2.stop()
        time.sleep(1)
        motor1.backward(0.8)
        motor2.backward(0.8)
        time.sleep(3)
        motor1.stop()
        motor2.stop()
        time.sleep(1)
        motor3.backward(0.8)
        motor4.backward(0.8)
        time.sleep(3)
        motor3.stop()
        motor4.stop()
        time.sleep(1)
        motor3.forward(0.6)
        motor4.forward(0.6)
        time.sleep(3)
        motor3.stop()
        motor4.stop()
        time.sleep(1)
        
        
        
        # for motor_name, motor in motors.items():
        #     print(f"Testing {motor_name}")
        #     motor.forward(0.5)  # Replace with motor.forward(speed) if using PWM
        #     time.sleep(2)
        #     motor.stop()
        #     time.sleep(1)

        # print("Done Testing")
    finally:
        print("Cleaning up")
        for motor_name, motor in motors.items():
            motor.close()
    GPIO.cleanup()