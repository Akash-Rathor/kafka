import socket
import threading
import os

LOG_FILE = "kafka_log.txt"

def append_to_log(message):
    """Append a message to the log file with an offset."""
    if not os.path.exists(LOG_FILE):
        offset = 0
    else:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            offset = len(lines)
    with open(LOG_FILE, "a") as f:
        f.write(f"offset:{offset} message:{message}\n")
    return offset

def read_from_log(offset):
    """Read the message at the given offset from the log file."""
    if not os.path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        if offset < len(lines):
            line = lines[offset]
            message = line.split("message:", 1)[1].strip()
            return message
        return None

def handle_client(client_socket, address):
    """Handle a client connection, supporting multiple requests."""
    print(f"New connection from {address}")
    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8").strip()
            if not data:  # Client disconnected
                break
            if data.startswith("PRODUCE"):
                # Handle producer: append message to log
                message = data[len("PRODUCE"):].strip()
                offset = append_to_log(message)
                client_socket.send(f"ACK offset:{offset}".encode("utf-8"))
                # Close connection for producers after one message (simplification)
                break
            elif data.startswith("CONSUME"):
                # Handle consumer: read message at offset
                try:
                    offset = int(data[len("CONSUME"):].strip())
                    message = read_from_log(offset)
                    if message:
                        client_socket.send(f"MESSAGE offset:{offset} {message}".encode("utf-8"))
                    else:
                        client_socket.send("NO_MESSAGE".encode("utf-8"))
                except ValueError:
                    client_socket.send("INVALID_OFFSET".encode("utf-8"))
            else:
                client_socket.send("INVALID_REQUEST".encode("utf-8"))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed for {address}")

def start_broker(host="localhost", port=9092):
    """Start the broker server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Broker started on {host}:{port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            # Handle each client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_broker()