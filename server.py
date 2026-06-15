import socket
import threading
from datetime import datetime

clients = {}  # {conn: username}

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

def broadcast(msg, sender=None):
    for client in list(clients):
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                remove_client(client)

def remove_client(conn):
    if conn in clients:
        username = clients[conn]
        del clients[conn]
        conn.close()
        broadcast(f"[{timestamp()}] *** {username} has left the chat ***")

def handle_client(conn, addr):
    try:
        conn.send("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()
        clients[conn] = username
        print(f"[+] {username} connected from {addr}")
        broadcast(f"[{timestamp()}] *** {username} joined the chat ***", conn)

        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break

            # Private message: /msg target_username hello
            if msg.startswith("/msg"):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    conn.send("Usage: /msg <username> <message>".encode())
                    continue
                target_name, private_msg = parts[1], parts[2]
                target_conn = next((c for c, u in clients.items() if u == target_name), None)
                if target_conn:
                    target_conn.send(f"[{timestamp()}] [PM from {username}]: {private_msg}".encode())
                    conn.send(f"[{timestamp()}] [PM to {target_name}]: {private_msg}".encode())
                else:
                    conn.send(f"User '{target_name}' not found.".encode())

            # List online users
            elif msg == "/users":
                user_list = ", ".join(clients.values())
                conn.send(f"Online: {user_list}".encode())

            else:
                formatted = f"[{timestamp()}] {username}: {msg}"
                print(formatted)
                broadcast(formatted, conn)

    except:
        pass
    finally:
        remove_client(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("[*] Server running on port 9999")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

start_server()