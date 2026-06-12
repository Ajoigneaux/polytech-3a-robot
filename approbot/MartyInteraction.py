from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal
from MartyCalibration import MartyCalibration

DEFAULT_IP = "192.168.1.2"

class MartyInteraction(QObject):

    def __init__(self):
        super().__init__()
        self.robot=None

        self.prec_angle_right_arm=0
        self.prec_angle_left_arm=0

    @Slot(Marty)
    def setRobot(self, robot_):
        self.robot=robot_

    @Slot(int)
    def moveUp(self, steps):
        self.robot.walk(num_steps=steps, step_length=25, move_time=1500,blocking=True)

    @Slot(int)
    def moveRight(self, steps):
        self.robot.sidestep(side="right", steps=steps, step_length=35, move_time=1000, blocking=True)

    @Slot(int)
    def moveDown(self, steps):
        self.robot.walk(num_steps=steps, step_length=-25, move_time=1500,blocking=True)

    @Slot(int)
    def moveLeft(self, steps):
        self.robot.sidestep(side="left", steps=steps, step_length=35, move_time=1000, blocking=True)

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
        self.prec_angle_left_arm=0
        self.prec_angle_right_arm=0
        self.robot.arms(left_angle=0, right_angle=0, move_time=500, blocking=False)

    @Slot(str)
    def eyesExpression(self, expr):#'angry', 'excited', 'normal', 'wide', or 'wiggle' 
        self.robot.eyes(pose_or_angle=expr, move_time=500, blocking=False)

    @Slot(str)
    def eyesColor(self, color_needed):#white, red, blue, yellow, green, teal, pink, purple, orange or hex value
        if color_needed=="off":
            print("YEUX OFF")
            self.robot.disco_off()
        elif color_needed=="rainbow":
            self.robot.disco_color(color="blue", region=0)
            self.robot.disco_color(color="yellow", region=1)
            self.robot.disco_color(color="red", region=2)
        else:
            self.robot.disco_color(color=color_needed, region="all")
