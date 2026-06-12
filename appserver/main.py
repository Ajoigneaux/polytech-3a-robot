import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from ServerManager import ServerManager

if __name__ == "__main__":
    QQuickStyle.setStyle("FluentWinUI3")
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    

    server_manager = ServerManager(8080)
    engine.rootContext().setContextProperty("server_manager", server_manager)

    engine.load("appserver/qml_interface/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    server_manager.stop()  # arrête proprement le serveur à la fermeture
    del engine
    sys.exit(exit_code)