import json
from urllib.parse import parse_qs, urlparse
import uuid

from PySide6.QtCore import QObject, QUrl, Signal, Slot
from http.server import BaseHTTPRequestHandler, HTTPServer
from Robot import Robot
from Battle import Battle
import threading
import socket

class ServerManager(QObject):

    #signaux envoyés à l'interface QML
    robotConnected = Signal(str)
    robotDisconnected = Signal(str)
    stepReceived = Signal(str,str,str,str,int,int) # rid, col, arm, exp, points, nb_steps
    logMessage = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.robots: dict[str, Robot] = {}
        self.battle = Battle()
        self.server = None
        self.thread = None
        self.host = ""

    serverStateChanged = Signal(bool)  # True = démarré, False = arrêté

    @Slot(result=str)
    def get_local_ip(self):
        try:
            s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
        
    @Slot(bool)
    def set_localhost(self, localhost: bool):
        if localhost :
            self.host = "127.0.0.1"
        else :
            self.host = ""
        

    @Slot()
    def start(self):
        if self.server is not None:
            return  # déjà démarré

        self.server = HTTPServer((self.host, self.port), self.make_handler())
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True  # le thread s'arrête si l'application se ferme
        self.thread.start()
        self.logMessage.emit(f"[INFO] Serveur démarré sur le port {self.port}")
        self.serverStateChanged.emit(True)

    @Slot()
    def stop(self):
        if self.server is None:
            return  # déjà arrêté

        self.server.shutdown()
        self.server = None
        self.thread = None
        self.logMessage.emit("[INFO] Serveur arrêté")
        self.serverStateChanged.emit(False)

    @Slot(str)
    def load_battle(self, filepath):
        clean_path = QUrl(filepath).toLocalFile()
        self.battle.load_file(clean_path)
        self.logMessage.emit(f"[BATTLE] Fichier chargé : {filepath}")

    def make_handler(self):
        manager = self

        class MyHandler(BaseHTTPRequestHandler):

            
            def send_json(self, data, code=200):
                body = json.dumps(data).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            
            @staticmethod #cette fonction est dans la classe mais elle n'a pas besoin de l'objet
            def parse_key_value(raw : bytes) -> dict:
                #Parse un champs data de type clé=valeur&clé=valeur
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError:
                    return {}
                params = parse_qs(text, keep_blank_values = True)
                return {k: v[0] for k, v in params.items()}
            
            def get_path_only(self):
                return urlparse(self.path).path
            
            def get_query_params(self):
                #Retourne les paramètres de query string sous forme de dict.
                parsed = urlparse(self.path)
                params = parse_qs(parsed.query)
                # parse_qs renvoie des listes ; on prend le premier élément
                return {k: v[0] for k, v in params.items()}
            
            def read_body(self):
                """Lit le corps de la requête et retourne un dict.
        
                Formats supportés (détectés via Content-Type) :
                - application/json                  -> JSON
                - application/x-www-form-urlencoded -> clé=valeur&clé=valeur
                - text/plain                        -> clé=valeur&clé=valeur
                - autre / absent                    -> tentative JSON, puis form-encoded
                """
                length = int(self.headers.get("Content-Length", 0))
                if length == 0:
                    return {}
        
                raw = self.rfile.read(length)
                content_type = self.headers.get("Content-Type", "")
        
                if "application/json" in content_type:
                    try:
                        return json.loads(raw)
                    except json.JSONDecodeError:
                        return {}
        
                if "application/x-www-form-urlencoded" in content_type or \
                "text/plain" in content_type:
                    return self.parse_key_value(raw)
        
                # Content-Type absent ou inconnu : on tente les deux
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return self.parse_key_value(raw)
            
            def log_message(self, fmt, *args):
                pass  # désactive les logs par défaut du HTTPServer pour utiliser les notres
            

            # Gestion des méthodes GET
            def do_GET(self):
                path = self.get_path_only()
                manager.logMessage.emit(f"REQUETE RECUE :  {path}")

                if path == "/":
                    self.send_json({"version" : "1.2"})

                elif path == "/score" :
                    params = self.get_query_params()
                    rid = params.get("rid")
                    if not rid or rid not in manager.robots:
                        self.send_json({"error" : "Robot inconnu"}, 404)
                        return
                    score = manager.robots[rid].score
                    manager.logMessage.emit(f"[SCORE] {rid} → {score} pts")
                    self.send_json({"score" : score})
                
                else:
                    self.send_json({"error" : "Methode GET inconnu "}, 404)

            # Gestion des méthodes POST
            def do_POST(self):
                path = self.get_path_only()
                manager.logMessage.emit(f"REQUETE RECUE :  {path}")

                if path == "/hello":
                    rid = str(uuid.uuid4())[:6].upper()
                    manager.robots[rid] = Robot(rid)
                    manager.robotConnected.emit(rid)
                    manager.logMessage.emit(f"[HELLO] Nouveau robot enregistré: {rid}")
                    self.send_json({"rid" : rid})

                elif path == "/start":
                    data = self.read_body()
                    rid = data.get("rid")
                    if not rid or rid not in manager.robots:
                        self.send_json({"error": "Robot inconnu"}, 404)
                        return
                    manager.robots[rid].reset()
                    manager.logMessage.emit(f"[START] {rid} démarre — {manager.battle.nb_moves} mouvements autorisés")
                    self.send_json({"moves": manager.battle.nb_moves})

                elif path == "/step":
                    data = self.read_body()
                    rid = data.get("rid")
                    col = data.get("col", "")
                    arm = data.get("arm", "")
                    exp = data.get("exp", "")
        
                    if not rid or rid not in manager.robots:
                        self.send_json({"error": "Robot inconnu"}, 404)
                        return
        
                    pts = manager.battle.calcul_step_score(col, arm, exp)
                    manager.robots[rid].add_step(col, arm, exp, pts)
                    nb_steps = len(manager.robots[rid].steps)
                    manager.logMessage.emit(f"[STEP] {rid} | col={col} arm={arm} exp={exp} -> +{pts} pts")
                    manager.stepReceived.emit(rid, col, arm, exp, pts, nb_steps)
                    self.send_json({"points": pts})

                elif path == "/bye":
                    data = self.read_body()
                    rid = data.get("rid")
                    if rid and rid in manager.robots:
                        manager.logMessage.emit(f"[BYE] {rid} déconnecté (score final : {manager.robots[rid].score})")
                        del manager.robots[rid]
                        manager.robotDisconnected.emit(rid)
                    self.send_response(200)
                    self.end_headers()
                
                else:
                    self.send_json({"error": "Methode POST inconnue"}, 404)
                
        return MyHandler