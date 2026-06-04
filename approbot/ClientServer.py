import requests

class ClientServer:
    def __init__(self, ip_server, port):
        self.url=f"http://{ip_server}:{port}"
        self.robot_id= None

    def check_server(self):
        try:
            r = requests.get(f"{self.url}/")
            return r.status_code == 200
        except requests.ConnectionError:
            return False