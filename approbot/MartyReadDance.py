from PySide6.QtCore import QObject, Slot, Signal, QTimer

class MartyReadDance(QObject):
    def __init__(self):
        super().__init__()
        self.dance_filename=""
        self.instruction_seq=[]

    def setDanceFile(self, filename):
        self.dance_filename=filename

    def readDanceFile(self):
        f = open(self.dance_filename)
        print(f.read())
