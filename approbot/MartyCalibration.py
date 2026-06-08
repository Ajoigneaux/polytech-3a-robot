from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal


class MartyCalibration(QObject) :

    calibrationColorPage=Signal()
    colors = []
    currentColor = ""
    robot = None

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

    @Slot()
    def calibrationColorPageSlot(self):
        self.calibrationColorPage.emit()

    @Slot(str)
    def calibrationColors(self, color):
        colorRead = self.robot.get_color_sensor_hex(self.robot, "left")
        colorHexa = "0x" + colorRead
        self.colors.append([color, colorHexa])

    @Slot()
    def whatIsThisColor(self):
        colorRead = self.robot.get_color_sensor_hex(self.robot, "left")
        colorReadHexa = "0x" + colorRead
        self.currentColor = self.findCloserColor(colorRead)

    
    def findCloserColor(self, curentColor):
        interval = 0x080808
        for color in self.colors:
            if int(curentColor, 16) < int(color[1], 16) + interval and int(curentColor, 16) > int(color[1], 16) - interval :
                # return color[0]
                print(color)
                return
        
    def setRobot(self, martyInteraction):#ENLEVER ????
        self.robot = martyInteraction.robot

    
        
