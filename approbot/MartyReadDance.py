from PySide6.QtCore import QObject, Slot, Signal, QTimer

class MartyReadDance(QObject):
    def __init__(self):
        super().__init__()
        self.dance_file_path=""
        self.instruction_seq=[]#[[nbr_step, step], ...]
        self.instruction_act={}#{'Color char': [action1, action2,...]}

    def setDanceFile(self, file_path):
        self.dance_file_path=file_path
        #clean_path = QUrl(filepath).toLocalFile()

    def readDanceFile(self):
        f = open(self.dance_file_path)
        dance_file=f.read().split('\n')
        dance_file.pop(0)
        act_index=dance_file.index("ACT")
        self.parseSequence(dance_file[:act_index])
        self.parseAct(dance_file[act_index+1:])

    def parseSequence(self, sequence_list):
        for mov in sequence_list:
            self.instruction_seq.append([mov[0], mov[1]])
    
    def parseAct(self, act_list):
        for act in act_list:
            splited_act=act.split(' ')
            self.instruction_act[splited_act[0]]=splited_act[1:]
        print(self.instruction_act)

    def startSequency(self, steps_number):#A BESOIN DU MODE BLOQUANT DES ACTIONS
        for i in range(steps_number):
            pass
            #Get movements
            #Execute movement
            #Check color sensor
            #Perform action associated
            #Send summary to server

    def executeMovement(self, mov, steps):
        match mov:
            case "U":
                #emit(steps, Direction ?)
                pass
            case "R":
                pass
            case "B":
                pass
            case "L":
                pass