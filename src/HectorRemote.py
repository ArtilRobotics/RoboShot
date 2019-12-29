from HectorAPI import HectorAPI
from LEDStripAPI import LEDStripAPI
import paho.mqtt.client as mqtt


class HectorRemote(HectorAPI, LEDStripAPI):

    def on_message(self, client, userdata, msg):
        print("REMOTE: on_message: " + msg.topic + ", " + msg.payload.decode("utf-8"))
        topic = msg.topic.replace(self.MainTopic, "")
        print(topic)
        if topic == "scale_readout/return":
            self.scale_read = int(msg.payload.decode("utf-8"))
            self.waiting_scale = False
        elif topic == "arm_position/return":
            self.arm_pos = int(msg.payload.decode("utf-8"))
            self.waiting_pos = False
        elif topic == "valve_dose/return":
            self.dose_sucessfull = not (msg.payload.decode("utf-8") == "-1")
            self.waiting_dose = False
        else:
            print("Unknown topic in HectorRemote")

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.MainTopic + "scale_readout/return")
        self.client.subscribe(self.MainTopic + "arm_position/return")
        self.client.subscribe(self.MainTopic + "valve_dose/return")

    def __init__(self):
        self.client = mqtt.Client()
        self.LEDTopic = "Hector9000/LEDStrip/"
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.MainTopic = "Hector9000/Hardware/"
        self.mqttip = "localhost"
        self.mqttport = 1883
        self.waiting_pos = False
        self.arm_pos = 0
        self.waiting_scale = False
        self.scale_read = 0
        self.waiting_dose = False
        self.dose_sucessfull = False
        self.client.connect(self.mqttip, self.mqttport, 60)
        self.client.loop_start()

    def pub_with_subtopic(self, topic, message="true"):
        self.client.publish(self.MainTopic + topic, message)

    def light_on(self):
        self.pub_with_subtopic("light_on")

    def light_off(self):
        self.pub_with_subtopic("light_off")

    def arm_out(self, cback=None):
        self.pub_with_subtopic("arm_out")

    def arm_in(self, cback=None):
        self.pub_with_subtopic("arm_in")

    def arm_isInOutPos(self):
        self.waiting_pos = True
        self.arm_pos = 0
        self.pub_with_subtopic("arm_position")
        while self.waiting_pos:
            pass
        return self.arm_pos

    def scale_readout(self):
        self.waiting_scale = True
        self.scale_read = 0
        self.pub_with_subtopic("scale_readout")
        while self.waiting_scale:
            pass
        return self.scale_read

    def scale_tare(self):
        self.pub_with_subtopic("scale_tare")

    def pump_start(self):
        self.pub_with_subtopic("pump_start")

    def pump_stop(self):
        self.pub_with_subtopic("pump_stop")

    def valve_open(self, index, open=1):
        self.pub_with_subtopic("valve_open")

    def valve_close(self, index):
        self.pub_with_subtopic("valve_close")

    def valve_dose(self, index, amount, timeout=30, cback=None, progress=(0,100), topic=""):
        self.waiting_dose = True
        self.dose_sucessfull = False
        self.pub_with_subtopic("valve_dose", str(index) + "," + str(amount) + "," + str(timeout))
        while self.waiting_dose:
            if self.client.want_write():
                self.client.loop_write()
            else:
                pass
        if not topic == "" and self.dose_sucessfull:
            full_process = progress[0] + progress[1]
            self.client.publish(topic, full_process)
            if full_process > 95:
                self.client.publish(topic, "end")
        else:
            if cback:
                cback(progress[0] + progress[1])
        return self.dose_sucessfull

    def finger(self, pos=0):
        self.pub_with_subtopic("finger")

    def ping(self, num, retract=True, cback=None):
        self.pub_with_subtopic("ping", "3")

    def cleanAndExit(self):
        self.pub_with_subtopic("clean_and_exit")

    def ledstripmessage(self,topic, color, type):
        message = str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "," + str(type)
        self.client.publish(self.LEDTopic + topic, message)

    def standart(self, color=(80, 80, 30), type=0):
        self.ledstripmessage("standart", color, type)

    def dosedrink(self, color=(20, 20, 255), type=0):
        self.ledstripmessage("dosedrink", color, type)

    def drinkfinish(self, color=(80, 80, 30), type=0):
        self.client.publish(self.LEDTopic + "drinkfinish", "true")

    def standby(self, color=(80,80,30), type=0):
        self.ledstripmessage("standby", color, type)
