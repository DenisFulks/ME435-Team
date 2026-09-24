import serial
import time

import PlateLoader

plateLoader = PlateLoader.PlateLoader("/dev/ttyACM0")
plateLoader.connect()

while True:
    print("Serial Menu")
    print("1 - RESET")
    print("2 - X-AXIS")
    print("3 - GRIPPER")
    print("4 - Z-AXIS")
    print("5 - MOVE")
    print("6 - EXIT")
    choice = input("Please Select a Command: ")

    if (choice == "1"):
        response = plateLoader.send_command("RESET")
        print(response)

    elif (choice == "2"):
        target = input("Where to (1-5):")
        response = plateLoader.send_command("X-AXIS " + target)
        print(response)

    elif (choice == "3"):
        while True:
            target = input("OPEN or CLOSE: ")
            if target == "OPEN" or target == "CLOSE":
                break
            else:
                print("Unrecognized Command")

        response = plateLoader.send_command("GRIPPER " + target)
        print(response)

    elif (choice == "4"):
        while True:
            target = input("EXTEND or RETRACT: ")
            if target == "EXTEND" or target == "RETRACT":
                break
            else:
                print("Unrecognized Command")

        response = plateLoader.send_command("Z-AXIS " + target)
        print(response)

    elif (choice == "5"):
        while True:
            plateFrom = input("From (1-5): ")
            if int(plateFrom) <= 5 and int(plateFrom) >= 1:
                break
            else:
                print("Unrecognized Position")

        while True:
            plateTo = input("To (1-5): ")
            if int(plateTo) <= 5 and int(plateFrom) >= 1:
                break
            else:
                print("Unrecognized Position")

        response = plateLoader.send_command("MOVE " + plateFrom + " " + plateTo)
        print(response)
    
    elif (choice == "6"):
        plateLoader.disconnect()
        break

    else:
        print("Command Not Recognized")

    print()