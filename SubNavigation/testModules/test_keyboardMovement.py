import keyboard
from modules.movement_mod import move_vertical, move_horizontal, turn, pitch

from time import sleep

# Movement functions and motor definitions are assumed to be imported or defined above

# Set default speed and duration variables
DEFAULT_SPEED = 0.5
DEFAULT_DURATION = 0.5

def handle_keypress():
    print("Controls: \n")
    print("W: Move Forward\nS: Move Backward\nA: Turn Left\nD: Turn Right")
    print("Q: Move Up\nE: Move Down\nZ: Pitch Up\nX: Pitch Down\nESC: Quit")

    while True:
        try:
            # Check if the ESC key is pressed to quit the program
            if keyboard.is_pressed("esc"):
                print("Exiting control program...")
                break

            # Horizontal movement: Forward (W) and Backward (S)
            if keyboard.is_pressed("w"):
                print("Moving Forward...")
                move_horizontal(forward=True, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            elif keyboard.is_pressed("s"):
                print("Moving Backward...")
                move_horizontal(forward=False, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            # Turning: Left (A) and Right (D)
            elif keyboard.is_pressed("a"):
                print("Turning Left...")
                turn(direction=True, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            elif keyboard.is_pressed("d"):
                print("Turning Right...")
                turn(direction=False, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            # Vertical movement: Up (Q) and Down (E)
            elif keyboard.is_pressed("q"):
                print("Moving Up...")
                move_vertical(up=True, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            elif keyboard.is_pressed("e"):
                print("Moving Down...")
                move_vertical(up=False, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            # Pitch: Up (Z) and Down (X)
            elif keyboard.is_pressed("z"):
                print("Pitching Up...")
                pitch(direction=True, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            elif keyboard.is_pressed("x"):
                print("Pitching Down...")
                pitch(direction=False, speed=DEFAULT_SPEED, duration=DEFAULT_DURATION)

            sleep(0.1)  # Prevent high CPU usage

        except KeyboardInterrupt:
            print("Program interrupted.")
            break

if __name__ == "__main__":
    print("Starting Submersible Vehicle Control Program...")
    handle_keypress()
