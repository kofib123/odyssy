
from gpiozero import Motor
from time import sleep

#///////////////// Define Motor Driver GPIO Pins /////////////////

FORWARD_1 = 27	# IN1 - Forward Drive 
REVERSE_1 = 22	# IN2 - Reverse Drive 
FORWARD_2 = 23	# IN3 - Forward Drive
REVERSE_2 = 24	# IN4 - Reverse Drive
# FORWARD_3 = 5
# REVERSE_3 = 6
# FORWARD_4 = 12
# REVERSE_4 = 16
# FORWARD_5 = 4
# REVERSE_5 = 17
# FORWARD_6 = 13
# REVERSE_6 = 26
motor1 = Motor(FORWARD_1, REVERSE_1) #GPIO: 27,22 (TOP_LEFT)
motor2 = Motor(FORWARD_2, REVERSE_2) #GPIO: 23,24 (TOP_RIGHT)
# motor3 = Motor(FORWARD_3, REVERSE_3) #GPIO: 5,6 (BACK_LEFT)
# motor4 = Motor(FORWARD_4, REVERSE_4) #GPIO: 12,16 (BACK_RIGHT)
# motor5 = Motor(FORWARD_5, REVERSE_5) #GPIO: 4,17 (BOTTOM_LEFT)
# motor6 = Motor(FORWARD_6, REVERSE_6) #GPIO: 13,26 (BOTTOM_RIGHT)

for i in range(1): 
    #FORWARD/BACKWARD: M5+M6
    motor1.forward(0.4)
    motor2.forward(0.4)
    sleep(5)
    motor1.stop()
    motor2.stop()
    #sleep(2)
    motor1.backward(0.4)
    motor2.backward(0.4)
    sleep(5)
    motor1.stop()
    motor2.stop()
    
    

#LEFT/RIGHT: M5-M6
#UP/DOWN: M1+M2+M3+M4+M5+M6
#PITCH: (M1+M2)-(M3+M4)
#ROLL: (M1+M3)-(M2+M4)