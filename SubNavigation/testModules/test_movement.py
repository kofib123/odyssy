import keyboard  # Requires `pip install keyboard`
from movement_module import move_vertical, move_horizontal, turn, pitch

def main():
    print("Control the submersible vehicle using the following keys:")
    print("W: Move forward")
    print("S: Move backward")
    print("A: Turn left (Yaw left)")
    print("D: Turn right (Yaw right)")
    print("Q: Move up")
    print("E: Move down")
    print("I: Pitch up")
    print("K: Pitch down")
    print("Press ESC to quit.")

    speed = 0.3  # Default speed (adjust as needed)
    duration = 0.5  # Default duration in seconds (adjust as needed)

    try:
        while True:
            if keyboard.is_pressed('w'):
                print("Moving forward...")
                move_horizontal(forward=True, speed=speed, duration=duration)

            if keyboard.is_pressed('s'):
                print("Moving backward...")
                move_horizontal(forward=False, speed=speed, duration=duration)

            if keyboard.is_pressed('a'):
                print("Turning left...")
                turn(direction=True, speed=speed, duration=duration)

            if keyboard.is_pressed('d'):
                print("Turning right...")
                turn(direction=False, speed=speed, duration=duration)

            if keyboard.is_pressed('q'):
                print("Moving up...")
                move_vertical(up=True, speed=speed, duration=duration)

            if keyboard.is_pressed('e'):
                print("Moving down...")
                move_vertical(up=False, speed=speed, duration=duration)

            if keyboard.is_pressed('i'):
                print("Pitching up...")
                pitch(direction=True, speed=speed, duration=duration)

            if keyboard.is_pressed('k'):
                print("Pitching down...")
                pitch(direction=False, speed=speed, duration=duration)

            if keyboard.is_pressed('esc'):
                print("Exiting control module...")
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")

if __name__ == "__main__":
    main()
