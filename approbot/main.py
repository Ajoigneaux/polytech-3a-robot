#PyQt Requirements
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from ClientServer import ClientServer
from MartyManager import MartyManager
from MartyInteraction import MartyInteraction
from MartyCalibration import MartyCalibration
from MartyReadDance import MartyReadDance

from PySide6.QtQuickControls2 import QQuickStyle

def connectSignals():
    marty_manager.robotUpdated.connect(marty_interaction.setRobot)
    marty_manager.robotUpdated.connect(marty_calibration.setRobot)

    marty_read_dance.moveUpRequested.connect(marty_interaction.moveUp)
    marty_read_dance.moveRightRequested.connect(marty_interaction.moveRight)
    marty_read_dance.moveBackRequested.connect(marty_interaction.moveDown)
    marty_read_dance.moveLeftRequested.connect(marty_interaction.moveLeft)

    marty_read_dance.eyesExpressionRequested.connect(marty_interaction.eyesExpression)
    marty_read_dance.eyesColorRequested.connect(marty_interaction.eyesColor)

    marty_read_dance.rightArmForwardRequested.connect(marty_interaction.rightArmForward)
    marty_read_dance.leftArmForwardRequested.connect(marty_interaction.leftArmForward)
    marty_read_dance.rightArmBackRequested.connect(marty_interaction.rightArmBack)
    marty_read_dance.leftArmBackRequested.connect(marty_interaction.leftArmBack)

if __name__ == "__main__":
    QQuickStyle.setStyle("FluentWinUI3")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    
    marty_manager = MartyManager()
    engine.rootContext().setContextProperty("marty_manager", marty_manager)

    marty_interaction = MartyInteraction()
    engine.rootContext().setContextProperty("marty_interaction", marty_interaction)

    client_server = ClientServer(8080)
    engine.rootContext().setContextProperty("client_server", client_server)

    
    marty_calibration = MartyCalibration()
    engine.rootContext().setContextProperty("marty_calibration", marty_calibration)

    marty_read_dance = MartyReadDance()
    engine.rootContext().setContextProperty("marty_read_dance", marty_read_dance)

    connectSignals()
    # POUR TESTER
    # marty_read_dance.setDanceFile("approbot/test.dance")
    # marty_read_dance.startSequency(10)

    # engine.loadFromModule("home_interface", "Main")
    engine.load("approbot/qml_interface/Main.qml")#Syntaxe plus légère pour le moment, mais pas de modularité

    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)