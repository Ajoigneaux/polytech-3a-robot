from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal, QTimer

DEFAULT_IP = "192.168.1.2"

class MartyInteraction(QObject):

    connectionToMartySuccess=Signal(bool)
    disconnectionToMartySuccess=Signal(bool)
    batteryLevelChanged=Signal(int)

    def __init__(self):
        super().__init__()
        self.robot=None
        self.battery=0
        #Timer for battery
        self.timer_battery = QTimer(self)
        self.timer_battery.setInterval(5000)  #Every 5 seconds
        self.timer_battery.timeout.connect(self.updateBattery)
        #Start timer after robot connection
        self.prec_angle_right_arm=0
        self.prec_angle_left_arm=0

    @Slot(str)
    def connect(self, ip_address):
        try:
            if(ip_address==""):
                ip_address=DEFAULT_IP
            self.robot=Marty("wifi", ip_address)
            print("Connexion to Marty at " + ip_address)
            self.connectionToMartySuccess.emit(True)
            #Battery update and start timer
            self.timer_battery.start()
            self.updateBattery()
        except:
            print("Failed to connect to Marty at : " + ip_address)
            self.connectionToMartySuccess.emit(False)

    @Slot()
    def disconnect(self):
        try:
            print("Disconnection to Marty")
            self.robot.close()
            self.disconnectionToMartySuccess.emit(True)
            self.timer_battery.stop();
        except:
            print("Disconnection to Marty failed")
            self.disconnectionToMartySuccess.emit(False)

    @Slot(result=int)
    def updateBattery(self):
        try:
            new_level = int(self.robot.get_battery_remaining())
            if(new_level!=self.battery):
                print(new_level)
                self.battery = new_level
                self.batteryLevelChanged.emit(new_level)
        except:
            print("Error on fetch battery level")

    @Slot()
    def moveUp(self):
        print("Up")
        self.robot.walk(num_steps=1, step_length=25, move_time=1500,blocking=False)

    @Slot()
    def moveRight(self):
        print("Right")
        self.robot.sidestep(side="right", steps=1, step_length=35, move_time=1000, blocking=False)

    @Slot()
    def moveDown(self):
        print("Down")
        self.robot.walk(num_steps=1, step_length=-25, move_time=1500,blocking=0)

    @Slot()
    def moveLeft(self):
        print("Left")
        self.robot.sidestep(side="left", steps=1, step_length=35, move_time=1000, blocking=False)

    @Slot()
    def rightArmForward(self):
        self.prec_angle_right_arm=100
        self.robot.arms(left_angle=self.prec_angle_left_arm, right_angle=100, move_time=500, blocking=False)

    @Slot()
    def leftArmForward(self):
        self.prec_angle_left_arm=100
        self.robot.arms(left_angle=100, right_angle=self.prec_angle_right_arm, move_time=500, blocking=False)

    @Slot()
    def rightArmBack(self):
        self.prec_angle_right_arm=-100
        self.robot.arms(left_angle=self.prec_angle_left_arm, right_angle=-100, move_time=500, blocking=False)

    @Slot()
    def leftArmBack(self):
        self.prec_angle_left_arm=-100
        self.robot.arms(left_angle=-100, right_angle=self.prec_angle_right_arm, move_time=500, blocking=False)

    @Slot()
    def resetArms(self):
        self.robot.arms(left_angle=0, right_angle=0, move_time=500, blocking=False)

    # my_marty.dance()
    # print(my_marty.wiggle(1000))
    # print(my_marty.get_battery_remaining())
    # my_marty.get_ready(True)
    # my_marty.walk(3,move_time=1000)
    # my_marty.send_file()
    # my_marty.get


    # print("test")
    # my_marty.close()

    # import requests

    # r = requests.get("http://192.168.0.105/")
    # print(r.status_code)
    # print(r.text)


    # r = requests.get("http://192.168.0.105/")
    # print(r.status_code)
    # print(r.text)

    # p = requests.post("http://192.168.0.105/hello")
    # print(p.status_code)
    # print(p.content)