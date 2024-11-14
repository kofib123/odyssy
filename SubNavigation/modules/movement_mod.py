
from gpiozero import Motor
from time import sleep 

#///////////////// Define Motor Driver GPIO Pins /////////////////

FORWARD_1, REVERSE_1 = 27, 22	# Buck1_IN1 - Forward Drive & Buck1_IN2 - Reverse Drive 
FORWARD_2, REVERSE_2 = 23, 24	# Buck1_IN3 - Forward Drive & Buck1_IN4 - Reverse Drive
FORWARD_3, REVERSE_3 = 5, 6     # Buck2_IN1 - Forward Drive & Buck2_IN2 - Reverse Drive
FORWARD_4, REVERSE_4 = 12, 16   # Buck2_IN3 - Forward Drive & Buck2_IN4 - Reverse Drive
FORWARD_5, REVERSE_5 = 4, 17    # Buck2_IN1 - Forward Drive & Buck2_IN2 - Reverse Drive
FORWARD_6, REVERSE_6 = 13, 26   # Buck2_IN3 - Forward Drive & Buck2_IN4 - Reverse Drive




motors = {
    "bottom_left": Motor(FORWARD_1, REVERSE_1),  #GPIO: 27,22 (bottom_LEFT) & GPIO: 23,24 (TOP_RIGHT) 
    "bottom_right" : Motor(FORWARD_2, REVERSE_2),  
    "front_left" : Motor(FORWARD_3, REVERSE_3), #GPIO: 5,6 (FRONT_LEFT) & GPIO: 12,16 (FRONT_RIGHT)
    "front_right" : Motor(FORWARD_4, REVERSE_4), 
    "back_left" : Motor(FORWARD_5, REVERSE_5), #GPIO: 4,17 (BACK_LEFT) & GPIO: 13,26 (BACK_RIGHT)
    "back_right" : Motor(FORWARD_6, REVERSE_6)
}


"""_summary_
    Turn all of the top motors ON at a given speed
"""
def move_vertical(up: bool, speed: float, duration: int):
    motorFL, motorFR = "front_left", "front_right" if up else "back_left", "back_right"
    motorBL, motorBR = "front_left", "front_right" if not up else "back_left", "back_right"
    #Move up at this point
    motors[motorFL].forward(speed)
    motors[motorFR].forward(speed)
    motors[motorBL].forward(speed)
    motors[motorBR].forward(speed)
    sleep(duration)
    #Reverse to stop movement
    motors[motorFL].reverse()
    motors[motorFR].reverse()
    motors[motorBL].reverse()
    motors[motorBR].reverse()
    sleep(1)
    # Stop the motion of motors
    motors[motorFL].stop()
    motors[motorFR].stop()
    motors[motorBL].stop()
    motors[motorBR].stop()
    
def move_horizontal(forward: bool, speed: float, duration: int):
    if forward:
        motors["bottom_left"].forward(speed)
        motors["bottom_right"].forward(speed)
    else:
        motors["bottom_left"].backward(speed)
        motors["bottom_right"].backward(speed)

    sleep(duration)
    motors["bottom_left"].reverse()
    motors["bottom_right"].reverse()
    sleep(1)
    motors["bottom_left"].stop()
    motors["bottom_right"].stop()

""" 
    This function will cause the motors to pivot on a point
    direction: True -> Left Turn, False -> Right Turn 
    duration: 
"""   
def turn(direction: bool, speed: float, duration: int):
    onMotor, diffMotor = "bottom_left", "bottom_right" if direction else "bottom_right", "bottom_left"
    motors[onMotor].forward(speed)
    motors[diffMotor].forward(0.2*speed)
    sleep(duration)
    motors[onMotor].stop()
    motors[diffMotor].stop()
    

# Pitch up -> True
# Pitch Down -> False
# motor forward left = motorFL
# motor backward left = motorBL
def pitch(direction: bool, speed: float, duration: int):
    motorFL, motorFR = "front_left", "front_right" if direction else "back_left", "back_right"
    motorBL, motorBR = "front_left", "front_right" if not direction else "back_left", "back_right"
        
    # This is the case where you want to pitch the vehicle up
    motors[motorFL].forward(speed)
    motors[motorFR].forward(speed)
    # This depends on the exquisite motion of the motors, if more differential thrust is needed, these values will be adjust
    motors[motorBL].backward(0.5 * speed)     # This depends 
    motors[motorBR].backward(0.5 * speed)
    sleep(duration) 

    motors[motorFL].reverse()
    motors[motorFR].reverse()
    motors[motorBL].reverse()
    motors[motorBR].reverse()
    sleep(1)
    
    motors[motorFL].stop()
    motors[motorFR].stop()
    motors[motorBL].stop()
    motors[motorBR].stop()
    return

#LEFT/RIGHT: M5-M6
#UP/DOWN: M1+M2+M3+M4+M5+M6
#PITCH: (M1+M2)-(M3+M4)
#ROLL: (M1+M3)-(M2+M4)