from server_http import *

if __name__ == "__main__":
    server = HTTPServer(ADDRESS, MyHandler)
    server.serve_forever()