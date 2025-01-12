import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import urllib.parse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
SECRET_KEY = os.urandom(32)  # 32-byte key for ChaCha20
IV = os.urandom(16)  # 16-byte nonce (128-bits) for ChaCha20

class FileUploadDownloadHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file_list()
        elif self.path.startswith("/download/"):
            self.download_file()
        else:
            return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']
        if "multipart/form-data" in content_type:
            boundary = content_type.split("=")[1].encode()
            content = self.rfile.read(content_length)
            # Split content by boundary and extract file data
            parts = content.split(b"--" + boundary)
            for part in parts:
                if b"Content-Disposition: form-data;" in part:
                    headers, file_data = part.split(b"\r\n\r\n", 1)
                    filename = self.extract_filename(headers)
                    if filename:
                        encrypted_data = self.encrypt_file(file_data)
                        file_path = os.path.join(UPLOAD_DIR, filename)
                        with open(file_path, "wb") as f:
                            f.write(encrypted_data)
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"File uploaded and encrypted successfully!")
                        return
        return self.send_response(400)

    def serve_file_list(self):
        # Get a list of files in the uploads directory
        files = os.listdir(UPLOAD_DIR)
        # Create a simple HTML to list files with download links
        html = """<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Uploaded Files</title>
        </head>
        <body>
        <h1>Upload a File</h1>
        <form method="POST" enctype="multipart/form-data" action="/">
        <input type="file" name="file" required>
        <button type="submit">Upload File</button>
        </form>
        <h2>Download Files</h2>
        <link rel="stylesheet" href="static/styles.css"> 
        <ul>"""
        for file in files:
            html += f'<li><a href="/download/{urllib.parse.quote(file)}">{file}</a></li>'
        html += """</ul>
        </body>
        </html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def download_file(self):
        filename = urllib.parse.unquote(self.path.split("/download/")[-1])
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", f"attachment; filename={filename}")
            self.end_headers()
            with open(file_path, "rb") as file:
                encrypted_data = file.read()
                decrypted_data = self.decrypt_file(encrypted_data)
                self.wfile.write(decrypted_data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def extract_filename(self, headers):
        header_str = headers.decode("utf-8")
        for line in header_str.split("\r\n"):
            if "filename=" in line:
                filename = line.split("filename=")[1].strip('"')
                return os.path.basename(filename)
        return None

    def encrypt_file(self, file_data):
        """Encrypt the file data using ChaCha20."""
        # Create ChaCha20 cipher
        cipher = Cipher(algorithms.ChaCha20(SECRET_KEY, IV), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        # Encrypt the data
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        return encrypted_data

    def decrypt_file(self, encrypted_data):
        """Decrypt the file data using ChaCha20."""
        # Create ChaCha20 cipher
        cipher = Cipher(algorithms.ChaCha20(SECRET_KEY, IV), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        # Decrypt the data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data

# HTTPS Configuration using SSLContext
server_address = ('', 8443)
httpd = HTTPServer(server_address, FileUploadDownloadHandler)

# Create SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print("HTTPS server running on https://localhost:8443...")
httpd.serve_forever()