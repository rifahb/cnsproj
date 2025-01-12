import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import urllib.parse

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileUploadDownloadHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # Serve the HTML form with links to available files
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
                        file_path = os.path.join(UPLOAD_DIR, filename)
                        with open(file_path, "wb") as f:
                            f.write(file_data.rstrip(b"\r\n"))
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"File uploaded successfully!")
                        return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid file upload request.")

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
        # Decode the URL path (to handle special characters like spaces)
        filename = urllib.parse.unquote(self.path.split("/download/")[-1])
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Debugging information
        print(f"Request to download: {self.path}")
        print(f"Decoded filename: {filename}")
        print(f"File path: {file_path}")
        
        # Check if the file exists and serve it
        if os.path.isfile(file_path):
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", f"attachment; filename={filename}")
            self.end_headers()
            with open(file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            print(f"File not found: {file_path}")  # Debugging information
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

# HTTPS Configuration using SSLContext
server_address = ('', 8443)
httpd = HTTPServer(server_address, FileUploadDownloadHandler)

# Create SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print("HTTPS server running on https://localhost:8443...")
httpd.serve_forever()
