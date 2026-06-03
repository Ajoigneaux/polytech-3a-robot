from http.server import BaseHTTPRequestHandler, HTTPServer
from Robot import Robot
from Battle import Battle
from urllib.parse import urlparse,parse_qs
import uuid
import json

VERSION = "1.1"
PORT = 8080
ADDRESS = ("", PORT)
robots : dict[str,Robot] = {}
battle = Battle()
battle.load_file("test.battle")

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
        #Retourne le chemin sans les paramètres de query.
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

    # Gestion des méthodes GET
    def do_GET(self):
        path = self.get_path_only()
        print(f"REQUETE RECUE : {path}")

        if path == "/":
            self.send_json({"version" : VERSION})

        elif path == "/score" :
            params = self.get_query_params()
            rid = params.get("rid")
            if not rid or rid not in robots:
                self.send_json({"error" : "Robot inconnu"}, 404)
                return
            print(f"[SCORE] {rid} -> {robots[rid].score} pts")
            self.send_json({"score" : robots[rid].score})
        
        else:
            self.send_json({"error" : "Methode GET inconnu "}, 404)

    # Gestion des méthodes POST
    def do_POST(self):
        path = self.get_path_only()
        print(f"POST reçu sur {path}")

        if path == "/hello":
            rid = str(uuid.uuid4())[:6].upper()
            robots[rid] = Robot(rid)
            print(f"[HELLO] Nouveau robot enregistré : {robots[rid]}")
            self.send_json({"rid" : rid})

        elif path == "/start":
            data = self.read_body()
            rid = data.get("rid")
            if not rid or rid not in robots:
                self.send_json({"error": "Robot inconnu"}, 404)
                return
            robots[rid].reset()
            print(f"[START] {rid} démarre — {battle.nb_moves} mouvements autorisés")
            self.send_json({"moves": battle.nb_moves})

        elif path == "/step":
            data = self.read_body()
            rid = data.get("rid")
            col = data.get("col", "")
            arm = data.get("arm", "")
            exp = data.get("exp", "")
 
            if not rid or rid not in robots:
                self.send_json({"error": "Robot inconnu"}, 404)
                return
 
            pts = battle.calcul_step_score(col, arm, exp)
            robots[rid].add_step(col, arm, exp, pts)
            print(f"[STEP]  {rid} | col={col} arm={arm} exp={exp} -> +{pts} pts "
                  f"(total={robots[rid].score})")
            self.send_json({"points": pts})

        elif path == "/bye":
            data = self.read_body()
            rid = data.get("rid")
            if rid and rid in robots:
                print(f"[BYE]   {rid} déconnecté (score final : {robots[rid].score})")
                del robots[rid]
            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_json({"error": "Methode POST inconnue"}, 404)

    
