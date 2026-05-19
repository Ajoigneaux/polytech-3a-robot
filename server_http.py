from http.server import BaseHTTPRequestHandler, HTTPServer
from robot import Robot
from urllib.parse import urlparse,parse_qs
import uuid
import json

version = 1.1
port = 8080
address = ("", port)
robots : dict[str,Robot] = {}

class MyHandler(BaseHTTPRequestHandler):
    
    def _send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod #cette fonction est dans la classe mais elle n'a pas besoin de l'objet
    def _parse_form(raw : bytes) -> dict:
        #Parse un champs data de type clé=valeur&clé=valeur
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return {}
        params = parse_qs(text, keep_blank_values = True)
        return {k: v[0] for k, v in params.items()}
    
    def _path_only(self):
        #Retourne le chemin sans les paramètres de query.
        return urlparse(self.path).path

    def _get_query_params(self):
        #Retourne les paramètres de query string sous forme de dict.
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        # parse_qs renvoie des listes ; on prend le premier élément
        return {k: v[0] for k, v in params.items()}

    # Gestion des méthodes GET
    def do_GET(self):
        path = self._path_only()
        print(f"REQUETE RECUE : {path}")

        if path == "/":
            self._send_json({"version" : version})

        elif path == "/score" :
            params = self._get_query_params()
            rid = params.get("rid")
            if not rid or rid not in robots:
                self._send_json({"error" : "Robot inconnu"}, 404)
                return
            print(f"[SCORE] {rid} -> {robots[rid].score} pts")
            self._send_json({"score" : robots[rid].score})
        
        else:
            self._send_json({"error" : "Methode GET inconnu "}, 404)

    # Gestion des méthodes POST
    def do_POST(self):
        path = self._path_only()
        print(f"POST reçu sur {path}")

        if path == "/hello":
            rid = str(uuid.uuid4())[:6].upper()
            robots[rid] = Robot(rid)
            print(f"[HELLO] Nouveau robot enregistré : {robots[rid]}")
            self._send_json({"rid" : rid})
        
        else:
            self._send_json({"error": "Methode POST inconnue"}, 404)

    
if __name__ == "__main__":
    server = HTTPServer(address, MyHandler)
    server.serve_forever()