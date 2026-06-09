#PyQt Requirements
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from MartyManager import MartyManager
from MartyInteraction import MartyInteraction
from MartyCalibration import MartyCalibration
from MartyReadDance import MartyReadDance

from PySide6.QtQuickControls2 import QQuickStyle

def connectSignals():
    marty_read_dance.moveUpRequested.connect(marty_interaction.moveUp)

if __name__ == "__main__":
    QQuickStyle.setStyle("FluentWinUI3")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    
    marty_manager = MartyManager()
    engine.rootContext().setContextProperty("marty_manager", marty_manager)

    marty_interaction = MartyInteraction(marty_manager.robot)
    engine.rootContext().setContextProperty("marty_interaction", marty_interaction)

    marty_calibration = MartyCalibration(marty_manager.robot)
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