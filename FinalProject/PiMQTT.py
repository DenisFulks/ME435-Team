import mqtt_helper as mh
import signal
import time
import gpiozero as gz

class App:
    
    def __init__(self):
        self.northButton = gz.Button(4)
        self.eastButton = gz.Button(17)
        self.southButton = gz.Button(27)
        self.westButton = gz.Button(22)

        self.leds = gz.LEDBoard(23, 18, 15, 14)

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/fulksdm/#",
                                publish_topic_name="me435/fulksdm/to_computer",
                                use_off_campus_broker=False)
        self.mqtt_client.callback = self.mqtt_callback

        self.northButton.when_pressed = lambda : self.mqtt_client.send_message("direction", "North")
        self.eastButton.when_pressed = lambda : self.mqtt_client.send_message("direction", "East")
        self.southButton.when_pressed = lambda : self.mqtt_client.send_message("direction", "South")
        self.westButton.when_pressed = lambda : self.mqtt_client.send_message("direction", "West")

    def decode_binary(self, value):
        binary = [0, 0, 0, 0]

        if value >= 8:
            binary[0] = 1
            value -= 8
        if value >= 4:
            binary[1] = 1
            value -= 4
        if value >= 2:
            binary[2] = 1
            value -= 2
        if value >= 1:
            binary[3] = 1
            value -= 2

        return binary

    def mqtt_callback(self, message_type, message_payload):
            print("Recieved type: ", message_type)
            print("Recieved payload: ", message_payload)

            if message_type == "score":
                binary = self.decode_binary(int(message_payload))
                self.leds.value = binary

def main():
    app = App()

    # counter = 0

    # while True:
    #     app.mqtt_client.send_message("score", counter)
    #     counter += 1
    #     if counter > 15:
    #         counter = 0
    #     time.sleep(0.5)

    signal.pause()

main()