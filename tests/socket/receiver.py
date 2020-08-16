from socket import create_server
import socket

HOST = '127.0.0.1'

PORT = 4000

print(f'Starting on http://{HOST}:{PORT}')

KEEP_ALIVE = True

while KEEP_ALIVE:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, address = s.accept()
        with conn:
            try:
                while True:
                    print('Receiving message...')
                    message = conn.recv(1024)
                    if not message: break
                    conn.sendall(b'Received message...')
            finally:
                # socket.close()
                pass

if __name__ == "__main__":
    pass