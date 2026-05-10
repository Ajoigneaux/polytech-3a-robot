#PyQt Requirements
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    # engine.loadFromModule("qml_interface", "Main")#Psser aux modules qml si besoin
    engine.load("qml_interface/Main.qml")#Syntaxe plus légère pour le moment, mais pas de modularité

    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)