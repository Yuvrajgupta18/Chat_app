import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"\n{msg}\nYou: ", end="")
        except:
            print("\n[Disconnected from server]")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    print("Commands: /msg <username> <text> for DM | /users to see who's online")
    while True:
        try:
            msg = input("You: ").strip()
            if msg:
                client.send(msg.encode())
        except KeyboardInterrupt:
            print("\n[Leaving chat]")
            client.close()
            break

start_client()