from PySide6.QtCore import QObject, Slot, Signal, QTimer

class MartyReadDance(QObject):

    #Movements signals
    moveUpRequested = Signal(int, bool)
    moveRightRequested = Signal(int, bool)
    moveBackRequested = Signal(int, bool)
    moveLeftRequested = Signal(int, bool)
    #Eyes signals
    eyesExpressionRequested = Signal(str)
    eyesColorRequested = Signal(str)
    #Arms positions
    rightArmForwardRequested = Signal()
    leftArmForwardRequested = Signal()
    rightArmBackRequested = Signal()
    leftArmBackRequested = Signal()
    resetArmsRequested = Signal()
    #Color management
    whatIsThisColorSignal=Signal()
    #Connection to server
    addExpressionToServer=Signal(str)
    addActionToServer=Signal(str)
    sendStep=Signal(str)
    getStepsNumber=Signal()

    def __init__(self):
        super().__init__()
        self.dance_file_path=""
        self.instruction_seq=[]#[[nbr_step, step], ...]
        self.instruction_act={}#{'Color char': [action1, action2,...]}
        self.currentColor = ""
        self.steps_number=0

    @Slot(str)
    def setCurrentColor(self, currentColor) :
        self.currentColor = currentColor

    @Slot(int)
    def setStepsNumber(self, steps_number):
        self.steps_number=steps_number

    @Slot(str)
    def setDanceFile(self, file_path):
        self.dance_file_path=file_path
        self.readDanceFile()

    def readDanceFile(self):
        f = open(self.dance_file_path)
        dance_file=f.read().split('\n')
        dance_file.pop(0)
        act_index=dance_file.index("ACT")
        self.instruction_seq=[] #Reset
        self.instruction_act={} #Reset
        self.parseSequence(dance_file[:act_index])
        self.parseAct(dance_file[act_index+1:])

    def parseSequence(self, sequence_list):
        for mov in sequence_list:
            self.instruction_seq.append([mov[0], mov[1]])
    
    def parseAct(self, act_list):
        for act in act_list:
            splited_act=act.split(' ')
            self.instruction_act[splited_act[0]]=splited_act[1:]

    @Slot()
    def startSequency(self):
        #Reset expressions
        self.eyesExpressionRequested.emit("normal")
        self.eyesColorRequested.emit("off")
        self.resetArmsRequested.emit()
        seq_len=len(self.instruction_seq)
        #Get steps number
        self.getStepsNumber.emit()
        #Delay ?
        for i in range(self.steps_number):
            print(f"Step : {i}")
            #Get movements
            steps, mov=self.instruction_seq[i%seq_len]
            #Execute movement
            self.executeMovement(mov, int(steps))
            #Check color sensor -> While marty.is_moving() ?
            self.whatIsThisColorSignal.emit()
            print(self.currentColor)
            #Perform action associated
            self.executeAction(self.currentColor)
            #MartyInteraction emit when finished actions ?
            #Send summary to server
            self.sendStep.emit(self.currentColor)

    def executeMovement(self, mov, steps):
        match mov:
            case "U":
                self.moveUpRequested.emit(steps, True)
                #Log ?
            case "R":
                self.moveRightRequested.emit(steps, True)
            case "B":
                self.moveBackRequested.emit(steps, True)
            case "L":
                self.moveLeftRequested.emit(steps, True)
    
    def executeAction(self, color_letter):#ex: color_letter="A"
        #Reset expressions
        self.eyesExpressionRequested.emit("normal")
        self.eyesColorRequested.emit("off")
        self.resetArmsRequested.emit()
        if color_letter in self.instruction_act:
            for act in self.instruction_act[color_letter]:
                self.decodeAction(act)

    def decodeAction(self, action):
        #Actions
        if action[0]=="A":
            match action[1:]:
                case "LU":
                    self.leftArmForwardRequested.emit()
                    self.addActionToServer.emit("ALU")
                case "RU":
                    self.rightArmForwardRequested.emit()
                    self.addActionToServer.emit("ARU")
                case "LB":
                    self.leftArmBackRequested.emit()
                    self.addActionToServer.emit("ALB")
                case "RB":
                    self.rightArmBackRequested.emit()
                    self.addActionToServer.emit("ARB")
        #Expressions
        if action[0]=="X":
            match action[1:]:
                case "NT":
                    self.eyesColorRequested.emit("#000000")
                    self.eyesExpressionRequested.emit("normal")
                    self.addExpressionToServer.emit("XNT")
                case "SD":
                    print("triste")
                    self.eyesColorRequested.emit("blue")
                    self.eyesExpressionRequested.emit("wide")
                    self.addExpressionToServer.emit("XSD")
                case "NG":
                    self.eyesColorRequested.emit("red")
                    self.eyesExpressionRequested.emit("angry")
                    self.addExpressionToServer.emit("XNG")
                case "HP":
                    self.eyesColorRequested.emit("green")
                    self.eyesExpressionRequested.emit("excited")
                    self.addExpressionToServer.emit("XHP")
                case "DN":
                    self.eyesExpressionRequested.emit("wiggle")
                    self.eyesColorRequested.emit("rainbow")
                    self.addExpressionToServer.emit("XDN")