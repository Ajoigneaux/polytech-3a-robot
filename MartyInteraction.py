from martypy import Marty
from PySide6.QtCore import QObject, Slot, Signal

class MartyInteraction(QObject):

    connectionToMartySuccess=Signal()

    def __init__(self):
        super().__init__()
        self.robot=None
        self.battery=0

    @Slot(str)
    def connect(self, ip_address):
        # self.robot=Marty("wifi", ip_address)
        print("Connexion to Marty at " + ip_address)
        self.connectionToMartySuccess.emit()
        self.battery=self.getBattery()

    @Slot(result=int)
    def getBattery(self):
        return 12#self.my_marty.get_battery_remaining()

    
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