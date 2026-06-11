from PySide6.QtCore import QObject, Slot, Signal, QTimer

class MartyReadDance(QObject):

    moveUpRequested = Signal(int)
    moveRightRequested = Signal(int)
    moveBackRequested = Signal(int)
    moveLeftRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self.dance_file_path=""
        self.instruction_seq=[]#[[nbr_step, step], ...]
        self.instruction_act={}#{'Color char': [action1, action2,...]}

    @Slot(str)
    def setDanceFile(self, file_path):
        self.dance_file_path=file_path
        #clean_path = QUrl(filepath).toLocalFile()
        self.readDanceFile()

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

    @Slot(int)
    def startSequency(self, steps_number):#A BESOIN DU MODE BLOQUANT DES ACTIONS ?
        for i in range(steps_number):
            #Get movements
            seq_len=len(self.instruction_seq)
            steps, mov=self.instruction_seq[i%seq_len]
            #Execute movement
            self.executeMovement(mov, int(steps))
            #Check color sensor
            # color_detected=???
            #Perform action associated
            # self.executeAction(color_detected)
            #MartyInteraction emit when finished actions ?
            #Send summary to server

    def executeMovement(self, mov, steps):
        match mov:
            case "U":
                self.moveUpRequested.emit(steps)
                #Log ?
            case "R":
                self.moveRightRequested.emit(steps)
            case "B":
                self.moveBackRequested.emit(steps)
            case "L":
                self.moveLeftRequested.emit(steps)
    
    def executeAction(self, color_letter):#ex: color_letter="A"
        if color_letter in self.instruction_act:
            for act in self.instruction_act[color_letter]:
                self.decodeAction(act)

    def decodeAction(self, action):
        #Actions
        if action[0]=="A":
            match action[1:]:
                case "LU":
                    pass
                case "RU":
                    pass
                case "LB":
                    pass
                case "RB":
                    pass
        #Expressions
        if action[0]=="X":
            match action[1:]:
                case "NT":
                    pass
                case "SD":
                    pass
                case "NG":
                    print("hungry detected")
                    pass
                case "HP":
                    pass
                case "DN":
                    pass