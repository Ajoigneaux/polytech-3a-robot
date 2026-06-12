from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal, QTimer

DEFAULT_IP = "192.168.1.2"

class MartyManager(QObject):

    connectionToMartySuccess=Signal(bool)
    disconnectionToMartySuccess=Signal(bool)
    robotUpdated=Signal(Marty)
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

    @Slot(str)
    def connect(self, ip_address):
        try:
            if(ip_address==""):
                ip_address=DEFAULT_IP
            self.robot=Marty("wifi", ip_address)
            print("Connexion to Marty at " + ip_address)
            self.connectionToMartySuccess.emit(True)
            self.robotUpdated.emit(self.robot)
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