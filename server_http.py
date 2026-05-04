from http.server import BaseHTTPRequestHandler, HTTPServer

port = 80
address = ("", port)

class MyHandler(BaseHTTPRequestHandler):
    def _set_header(self, code=200) :
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    # Gestion des méthodes GET
    def do_GET(self):
        print("REQUETE RECUE :", self.path)
        if self.path == "/":
            self._set_header()
            self.wfile.write(b"1.2")
        else :
            self._set_header(404)
    
server = HTTPServer(address,MyHandler)
server.serve_forever()