import socket
import threading
import os

HOST = '127.0.0.1'  
PORT = 65432        

clients = []
lock = threading.Lock()  

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            with lock:
                for client in clients:
                    if client != conn:
                        client.sendall(f'{addr}: {data}'.encode())

            print(f'{addr}: {data}')
        except Exception as e:
            print(f'Error handling client {addr}: {e}')
            clients.remove(conn)  
            break

    conn.close()
    print(f'Client {addr} disconnected')

def create_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            clients.append(conn)  
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        
        create_server()
    else:
        os.exit(0)
