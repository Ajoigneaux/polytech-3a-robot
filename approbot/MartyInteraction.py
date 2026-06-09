from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal
from MartyCalibration import MartyCalibration

DEFAULT_IP = "192.168.1.2"

class MartyInteraction(QObject):

    calibrationColorPage=Signal()

    def __init__(self, robot_):
        super().__init__()
        self.robot=robot_

        self.prec_angle_right_arm=0
        self.prec_angle_left_arm=0

    @Slot(int)
    def moveUp(self, steps=1):
        print("Up")
        self.robot.walk(num_steps=steps, step_length=25, move_time=1500,blocking=False)

    @Slot(int)
    def moveRight(self, steps=1):
        print("Right")
        self.robot.sidestep(side="right", steps=steps, step_length=35, move_time=1000, blocking=False)

    @Slot(int)
    def moveDown(self, steps=1):
        print("Down")
        self.robot.walk(num_steps=steps, step_length=-25, move_time=1500,blocking=0)

    @Slot(int)
    def moveLeft(self, steps=1):
        print("Left")
        self.robot.sidestep(side="left", steps=steps, step_length=35, move_time=1000, blocking=False)

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