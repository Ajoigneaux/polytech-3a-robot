#PyQt Requirements
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

#Signal et slot pour interactions
from PySide6.QtCore import QObject, Slot

class Console(QObject):
    @Slot(str)
    def outputStr(self, s):
        print(s)

con=Console()
#Fin signal et slot

from MartyInteraction import MartyInteraction

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.rootContext().setContextProperty("con", con)#Connexion du signal

    marty_interaction = MartyInteraction()
    engine.rootContext().setContextProperty("marty_interaction", marty_interaction)
    # engine.loadFromModule("home_interface", "Main")
    engine.load("qml_interface/Main.qml")#Syntaxe plus légère pour le moment, mais pas de modularité

    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)