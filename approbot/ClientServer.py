import requests
from PySide6.QtCore import QObject, Slot, Signal

class ClientServer(QObject):

    serverConnected = Signal(bool)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.url = ""
        self.rid= None

    @Slot(str)
    def checkServer(self, ip_server):
        self.url=f"http://{ip_server}:{self.port}"
        print(f"{self.url}")
        try:
            r = requests.get(f"{self.url}/")
            if(r.status_code == 200):
                self.hello()
                print(f"[SERVER] Connecté, rid : {self.rid}")
                self.serverConnected.emit(True)
                
        except requests.ConnectionError:
            print("[SERVER] Connexion échouée")
            self.serverConnected.emit(False)

    def hello(self):
        r = requests.post(f"{self.url}/hello")
        self.rid = r.json()["rid"]

    def start(self):
        r = requests.post(f"{self.url}/start", json={"rid": self.rid})
        return r.json()["moves"]
    
    def step(self, col, arm, exp):
        r = requests.post(f"{self.url}/step", json={
            "rid": self.rid, "col": col, "arm": arm, "exp": exp
        })
        return r.json()["points"]
    
    def score(self):
        r = requests.get(f"{self.url}/score", params={"rid": self.rid})
        return r.json()["score"]
    
    @Slot()
    def bye(self):
        requests.post(f"{self.url}/bye", json={"rid": self.rid})
        self.rid = None
        print(f"[CLIENT] Déconnecté du serveur")
    
    
    
