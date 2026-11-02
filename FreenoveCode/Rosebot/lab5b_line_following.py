from rosebot import Rosebot
import time

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()

    fastSpeed = 12
    slowSpeed = 5

    try:
        while robot.ultrasonic.get_cm() > 20:
            print(robot.ultrasonic.get_cm())
            print(robot.line_sensors.get_line_word())

            if (robot.line_sensors.get_left() == "B"):
                robot.drive_system.set_speeds(slowSpeed, slowSpeed, fastSpeed, fastSpeed)
            elif (robot.line_sensors.get_right() == "B"):
                robot.drive_system.set_speeds(fastSpeed, fastSpeed, slowSpeed, slowSpeed)
            else:
                robot.drive_system.set_speeds(fastSpeed, fastSpeed, fastSpeed, fastSpeed)

        robot.drive_system.stop()

    except KeyboardInterrupt:
        # Handle Ctrl-C to exit the program
        robot.drive_system.stop()
        print("Goodbye!")

main()