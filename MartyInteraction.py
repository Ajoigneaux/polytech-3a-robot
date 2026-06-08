from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal
from MartyCalibration import MartyCalibration

class MartyInteraction(QObject):

    connectionToMartySuccess=Signal(bool)
    disconnectionToMartySuccess=Signal(bool)
    calibrationColorPage=Signal()
    marty_calibration = ""

    def __init__(self):
        super().__init__()
        self.robot=None
        self.battery=0

    @Slot(str)
    def connect(self, ip_address):
        try:
            if(ip_address==""):
                self.robot=Marty("wifi", "192.168.1.2")
            else:
                self.robot=Marty("wifi", ip_address)
            print("Connexion to Marty at " + ip_address)
            self.connectionToMartySuccess.emit(True)
            self.battery=self.getBattery()
            self.marty_calibration = MartyCalibration(self.robot)



        except:
            print("Failed to connect to Marty at : " + ip_address)
            self.connectionToMartySuccess.emit(False)

    @Slot()
    def disconnect(self):
        try:
            print("Disconnection to Marty")
            self.robot.close()
            self.disconnectionToMartySuccess.emit(True)
        except:
            print("Disconnection to Marty failed")
            self.disconnectionToMartySuccess.emit(False)

                
    @Slot()
    def calibrationColorPageSlot(self):
        self.calibrationColorPage.emit()


    @Slot(result=int)
    def getBattery(self):
        return 12#self.my_marty.get_battery_remaining()
        
    @Slot(str)
    def callCalibrationfunction(self, color):
        self.marty_calibration.calibrationColors(color)

    @Slot()
    def callWhatIsThiColorFunction(self):
        self.marty_calibration.whatIsThisColor()



    
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