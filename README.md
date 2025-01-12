# Secure Custom HTTP Server

## Introduction

The **Secure Custom HTTP Server** is a secure file upload and download platform that ensures the protection of sensitive data through encryption. This server leverages secure encryption algorithms like ChaCha20 for encrypting uploaded files and ensuring that they are securely transmitted over HTTPS. The server also provides a simple yet efficient interface for users to upload, download, and access files while maintaining high security.

The server runs over HTTPS with SSL/TLS encryption, ensuring that the communication between the server and the client remains private and secure. It also includes functionality for encrypting file uploads and decrypting file downloads using advanced cryptographic techniques.

## Objectives

The primary objectives of the **Secure Custom HTTP Server** are:
- To provide a secure and encrypted platform for file uploads and downloads.
- To ensure that all file transfers are done over HTTPS for security.
- To implement encryption and decryption of files using ChaCha20 encryption algorithm.
- To create an intuitive and simple user interface for interacting with the server.
- To serve as a learning platform for cryptography and server-side web application development.

## Methodology Used

The **Secure Custom HTTP Server** follows a secure methodology to handle file uploads and downloads. Here's an overview of the methodology used:

1. **File Upload and Encryption**:
   - The server accepts file uploads from clients using a simple HTTP POST request with `multipart/form-data`.
   - Files are encrypted using the **ChaCha20** encryption algorithm with a securely generated 32-byte key and a 16-byte nonce (IV).
   - The encrypted files are stored in a secure directory on the server.

2. **File Download and Decryption**:
   - When users request a file for download, the server sends the encrypted file.
   - Upon downloading, the file is decrypted using the same ChaCha20 key and IV before it is sent to the user.

3. **Secure HTTPS Communication**:
   - The server runs over **HTTPS**, ensuring all data transmitted between the client and server is encrypted and secure.
   - SSL/TLS certificates are used to secure the server and client communication.

4. **File Listing and Simple Web Interface**:
   - The server also lists all uploaded files on a web page, allowing users to easily download or upload files.

## Technology Stack

- **Python**: The core programming language for the server-side implementation.
- **HTTPServer**: Built-in module used for setting up the HTTP server.
- **SSL/TLS**: Secure Sockets Layer (SSL) and Transport Layer Security (TLS) protocols for secure communication.
- **ChaCha20 Encryption**: Cryptographic algorithm for file encryption and decryption.
- **cryptography**: A Python package used for cryptographic operations, such as encryption and decryption.
- **HTML**: For rendering the file upload/download interface.
- **SSLContext**: Used to load SSL certificates and establish secure HTTPS connections.

## Comparison to Existing Solution

### Existing Solutions:
1. **Cloud Storage Services (e.g., Google Drive, Dropbox)**:
   - These services provide file storage, but they may not provide full encryption of user files at rest and during transit.
   - They typically require accounts and third-party dependencies.

2. **Basic HTTP Servers**:
   - Many simple HTTP servers exist that offer file upload and download, but they lack built-in encryption for file storage and transmission.
   - Security is often not a priority for basic HTTP servers.

### Advantages of Our Solution:
- **End-to-End Encryption**: Unlike cloud storage services that may store user files without encryption, our solution ensures that all files are encrypted before being stored and decrypted when downloaded.
- **Customizable**: The solution is fully customizable, providing more control over the encryption method and file storage.
- **Lightweight and Self-Hosted**: Unlike large third-party cloud services, this server can be hosted locally, offering more privacy and control over the files.
- **No User Accounts Required**: The solution doesn’t require user accounts, keeping the system simple and efficient while maintaining security.

## Results

The **Secure Custom HTTP Server** has successfully implemented the following features:
- **Secure File Uploads and Downloads**: Files are encrypted before upload and decrypted before download, ensuring that no unauthorized access occurs.
- **HTTPS Support**: The server uses SSL/TLS certificates to ensure secure communication over the internet.
- **File Listing Interface**: A simple web interface allows users to view available files and download them securely.
- **Encryption Performance**: The use of ChaCha20 encryption ensures fast encryption and decryption times while maintaining a high level of security.

## Screenshots
![WhatsApp Image 2025-01-12 at 21 57 07](https://github.com/user-attachments/assets/bb0f26fa-415d-4b8b-9e7d-ef18ea309c2b)

![CBFFA5DA-C1E9-4AE4-9E8B-69CCBA43E8D2](https://github.com/user-attachments/assets/b6c94f0d-50e5-455f-857a-b42311f12582)

![WhatsApp Image 2025-01-12 at 21 59 37](https://github.com/user-attachments/assets/0ac58bb0-b40a-46df-a121-7ca70ce1aa48)


## References

1. **ChaCha20 Encryption Algorithm**: https://en.wikipedia.org/wiki/ChaCha20
2. **cryptography Library**: https://cryptography.io/en/latest/
3. **Python HTTPServer Documentation**: https://docs.python.org/3/library/http.server.html
4. **SSL/TLS Protocols**: https://en.wikipedia.org/wiki/Transport_Layer_Security
5. **Python SSLContext**: https://docs.python.org/3/library/ssl.html
