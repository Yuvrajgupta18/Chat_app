# Chat App — Multi-Client TCP Chat Server

A real-time terminal-based chat application built with Python using TCP sockets and multithreading. Multiple clients can connect to a central server and exchange messages simultaneously.

## Features

- Multi-client support — multiple users can chat at the same time
- Real-time broadcasting — messages instantly delivered to all connected users
- Private messaging — send DMs using `/msg <username> <message>`
- Online users list — see who's connected using `/users`
- Timestamps — every message shows the time it was sent
- Graceful disconnect — server notifies everyone when a user leaves

## Tech Stack

- Python 3
- `socket` — TCP connection management
- `threading` — one thread per client for concurrent connections

## How It Works

1. Server binds to a port and listens for incoming TCP connections
2. Each new client connection spawns a dedicated thread
3. Server maintains a dictionary of active clients `{connection: username}`
4. Messages are broadcast to all clients except the sender
5. On disconnect, client is removed and others are notified

## Setup & Run

**Start the server:**
```bash
python3 server.py
```

**Connect as a client (open a new terminal for each user):**
```bash
python3 client.py
```

## Commands

| Command | Description |
|--------|-------------|
| `/msg <username> <message>` | Send a private message |
| `/users` | List all online users |

## Concepts Demonstrated

- TCP socket lifecycle: bind → listen → accept → send/recv
- Multithreading for concurrent client handling
- Network addressing (IP + port)
- Error handling for unexpected client disconnects

## Project Structure

```
chat-app/
├── server.py   # Handles connections, threading, broadcasting
├── client.py   # Connects to server, sends/receives messages
└── README.md
```
