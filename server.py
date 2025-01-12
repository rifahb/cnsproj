import os
import ssl
import base64
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CustomWebServer(SimpleHTTPRequestHandler):
    USERNAME = "admin1"
    PASSWORD = "password"

    def do_GET(self):
        # Basic Authentication
        auth_header = self.headers.get('Authorization')
        if not auth_header or not self.is_authenticated(auth_header):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Custom Web Server"')
            self.end_headers()
            self.wfile.write(b"Authentication required.")
            return

        # Serve Static Files from the /static directory
        if self.path == "/":
            self.path = "/index.html"
        file_path = os.path.join(os.getcwd(), "static", self.path.lstrip("/"))
        if os.path.isfile(file_path):
            self.send_response(200)
            self.send_header("Content-type", self.guess_type(file_path))
            self.end_headers()
            with open(file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")

    def is_authenticated(self, auth_header):
        try:
            auth_type, credentials = auth_header.split(' ', 1)
            if auth_type != "Basic":
                return False
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(":", 1)
            return username == self.USERNAME and password == self.PASSWORD
        except Exception as e:
            return False


def run_server():
    server_address = ('', 8443)
    httpd = HTTPServer(server_address, CustomWebServer)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    # Wrap the socket with the context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Custom HTTPS server running on https://localhost:8443...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
