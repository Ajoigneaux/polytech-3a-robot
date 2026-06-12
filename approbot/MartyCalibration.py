from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal


class MartyCalibration(QObject) :

    currentColorDetectedSignal=Signal(str)
    colors = {}
    currentColor = ""

    def __init__(self):
        super().__init__()
        self.robot = None

    @Slot(Marty)
    def setRobot(self, robot_):
        self.robot=robot_

    @Slot(str)
    def calibrationColors(self, color):
        colorRead = self.robot.get_color_sensor_hex("left")
        colorHexa = "0x" + colorRead
        self.colors[color] = colorHexa



    @Slot()
    def whatIsThisColor(self):
        colorRead = self.robot.get_color_sensor_hex("left")
        colorReadHexa = "0x" + colorRead
        self.currentColor = self.findCloserColor(colorReadHexa)
        self.currentColorDetectedSignal.emit(self.currentColor)

    
    def findCloserColor(self, curentColor):
        interval = 0x080808
        for color in self.colors.items():
            # print(color[0])
            if int(curentColor, 16) < int(color[1], 16) + interval and int(curentColor, 16) > int(color[1], 16) - interval :
                return color[0]

    
        
