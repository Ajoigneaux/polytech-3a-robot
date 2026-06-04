import requests
from PySide6.QtCore import QObject, Slot

class ClientServer(QObject):
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
                print(f"{self.rid}")
                
        except requests.ConnectionError:
            print("connection failed")

    def hello(self):
        r = requests.post(f"{self.url}/hello")
        self.rid = r.json()["rid"]

        
    
    
