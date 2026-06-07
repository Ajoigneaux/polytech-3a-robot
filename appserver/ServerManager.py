from PySide6.QtCore import QObject, Signal, Slot
from http.server import HTTPServer
from Robot import Robot
from Battle import Battle
import threading

class ServerManager(QObject):

    #signaux envoyés à l'interface QML
    robotConnected = Signal(str)
    robotDisconcted = Signal(str)
    stepReceived = Signal(str,str,str,str,int) # rid, col, arm, exp, points
    logMessage = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.robots = dict[str, Robot] = {}
        self.battle = Battle()
        self.server = None
        self.thread = None

    @Slot()
    def start(self):
        if self.server is not None:
            return  # déjà démarré

        self.server = HTTPServer(("", self.port), MyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True  # le thread s'arrête si l'application se ferme
        self.thread.start()
        self.logMessage.emit(f"Serveur démarré sur le port {self.port}")

    @Slot()
    def stop(self):
        if self.server is None:
            return  # déjà arrêté

        self.server.shutdown()
        self.server = None
        self.thread = None
        self.logMessage.emit("Serveur arrêté")

    @Slot(str)
    def load_battle(self, filepath):
        self.battle.load_file(filepath)
        self.logMessage.emit(f"[BATTLE] Fichier chargé : {filepath}")