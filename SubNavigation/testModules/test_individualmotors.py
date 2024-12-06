import time

# Back_left and Back_right
FORWARD_5, REVERSE_5 = 4, 17    # Buck2_IN1 - Forward Drive & Buck2_IN2 - Reverse Drive A
FORWARD_6, REVERSE_6 = 13, 26   # Buck2_IN3 - Forward Drive & Buck2_IN4 - Reverse Drive B

#Front_left and Front_right
FORWARD_3, REVERSE_3 = 5, 6     # Buck2_IN1 - Forward Drive & Buck2_IN2 - Reverse Drive D
FORWARD_4, REVERSE_4 = 12, 16   # Buck2_IN3 - Forward Drive & Buck2_IN4 - Reverse Drive C

FORWARD_1, REVERSE_1 = 27, 22	# Buck1_IN1 - Forward Drive & Buck1_IN2 - Reverse Drive E
FORWARD_2, REVERSE_2 = 23, 24	# Buck1_IN3 - Forward Drive & Buck1_IN4 - Reverse Drive F



""" 
motors dict stores the Motor objects as values 
"""
motors = {
    "motorE": Motor(FORWARD_1, REVERSE_1),  #GPIO: 27,22 (bottom_LEFT) & GPIO: 23,24 (bottom_RIGHT) 
    "motorF" : Motor(FORWARD_2, REVERSE_2),  
    "motorD" : Motor(FORWARD_3, REVERSE_3), #GPIO: 5,6 (FRONT_LEFT) & GPIO: 12,16 (FRONT_RIGHT)
    "motorC" : Motor(FORWARD_4, REVERSE_4), 
    "motorA" : Motor(FORWARD_5, REVERSE_5), #GPIO: 4,17 (BACK_LEFT) & GPIO: 13,26 (BACK_RIGHT)
    "motorB" : Motor(FORWARD_6, REVERSE_6)
}

if __name__ == "__main__":
    speed = 0.5
    print("Testing Motor A")
    motors["motorA"].forward(speed)
    time.sleep(2)
    motors["motorA"].stop()
    time.sleep(1)
    
    print("Testing Motor B")
    motors["motorB"].forward(speed)
    time.sleep(2)
    motors["motorB"].stop()
    time.sleep(1)
    
    print("Testing Motor C")
    motors["motorC"].forward(speed)
    time.sleep(2)
    motors["motorC"].stop()
    time.sleep(1)
    
    print("Testing Motor D")
    motors["motorD"].forward(speed)
    time.sleep(2)
    motors["motorD"].stop()
    time.sleep(1)
    
    print("Testing Motor E")
    motors["motorE"].forward(speed)
    time.sleep(2)
    motors["motorE"].stop()
    time.sleep(1)
    
    print("Testing Motor F")
    motors["motorF"].forward(speed)
    time.sleep(2)
    motors["motorF"].stop()
    time.sleep(1)
    
    print("Done Testing")
    