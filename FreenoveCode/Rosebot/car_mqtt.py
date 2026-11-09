from rosebot import Rosebot
import mqtt_helper as mh
import gpiozero as gz
import time
import datetime

class App:

    def __init__(self):
        self.robot = Rosebot()

        self.is_streaming = False
        self.mode = "none"

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/fulksdm/#",
                                publish_topic_name="me435/fulksdm/to_computer",
                                use_off_campus_broker=False)
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):
        print("Recieved type: ", message_type)
        print("Recieved payload: ", message_payload)

        if message_type == "set_speeds":
            self.robot.drive_system.set_speeds(message_payload[0], message_payload[1], message_payload[2], message_payload[3]) 

        if message_type == "stop":
            self.robot.drive_system.stop() 

        if message_type == "beep":
            self.robot.buzzer.beep(on_time=0.1, off_time=0.3, n=2)  

        if message_type == "is_streaming":
            self.is_streaming = message_payload

        if message_type == "mode":
            self.mode = message_payload
            if self.mode == "drive_until_wall" or self.mode == "drive_until_line":
                self.robot.drive_system.go(25, 25)
            if self.mode == "none":
                self.robot.drive_system.stop()


def main():
    print("Rosebot MQTT")
    app = App()
    last_time_sent_s = 0

    time.sleep(2)
    # app.mqtt_client.send_message("is_streaming", True)
    # app.mqtt_client.send_message("mode", "line_following")

    fastSpeed = 12
    slowSpeed = 0

    try:
        while True:
            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()

            if app.is_streaming and current_time_s > last_time_sent_s + 2:
                last_time_sent_s = current_time_s
                app.mqtt_client.send_message("line_sensor_reading", {
                    "timestamp": right_now.strftime("%m/%d/%Y  %H:%M:%S"),
                    "left": app.robot.line_sensors.get_left(),
                    "middle": app.robot.line_sensors.get_middle(),
                    "right": app.robot.line_sensors.get_right(),
                })

            if app.mode == "drive_until_wall" and app.robot.ultrasonic.get_cm() < 20:
                app.robot.drive_system.stop()
                app.robot.buzzer.beep(on_time=0.1, off_time=0.1, n=3)
                app.mode = "none"

            if app.mode == "drive_until_line" and app.robot.line_sensors.get_line_word() == "BBB":
                app.robot.drive_system.stop()
                app.robot.buzzer.beep(on_time=0.1, off_time=0.1, n=3)
                app.mode = "none"

            if app.mode == "line_following":
                if (app.robot.line_sensors.get_left() == "B"):
                    app.robot.drive_system.set_speeds(slowSpeed, slowSpeed, fastSpeed, fastSpeed)
                elif (app.robot.line_sensors.get_right() == "B"):
                    app.robot.drive_system.set_speeds(fastSpeed, fastSpeed, slowSpeed, slowSpeed)
                else:
                    app.robot.drive_system.set_speeds(fastSpeed, fastSpeed, fastSpeed, fastSpeed)

    except KeyboardInterrupt:
        print("Goodbye")
        app.robot.drive_system.stop()
        app.mqtt_client.close()

main()