import socket
import time

class KafkaConsumer:
    def __init__(self, host="localhost", port=9092):
        self.host = host
        self.port = port
        self.offset = 0
        self.client_socket = None

    def connect(self):
        """Connect to the broker, reusing the existing socket if possible."""
        if self.client_socket is None:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                print(f"Connected to broker at {self.host}:{self.port}")
            except Exception as e:
                print(f"Failed to connect: {e}")
                self.client_socket = None
                return False
        return True

    def read(self):
        """Read messages from the broker using a persistent connection."""
        print("Consumer started. Waiting for data...")
        while True:
            if not self.connect():  # Ensure connected
                time.sleep(2)  # Wait before retrying
                continue
            try:
                # Send CONSUME request with current offset
                self.client_socket.send(f"CONSUME {self.offset}".encode("utf-8"))
                # Receive response
                response = self.client_socket.recv(1024).decode("utf-8").strip()
                if not response:  # Broker disconnected
                    print("Broker disconnected")
                    self.client_socket.close()
                    self.client_socket = None
                    continue
                if response.startswith("MESSAGE"):
                    parts = response.split(" ", 2)
                    offset = int(parts[1].split(":")[1])
                    message = parts[2]
                    print(f"Consumed: {message} (offset: {offset})")
                    self.offset = offset + 1
                elif response == "NO_MESSAGE":
                    pass  # No new messages
                else:
                    print(f"Broker response: {response}")
                time.sleep(1)  # Poll every second
            except Exception as e:
                print(f"Error: {e}")
                self.client_socket.close()
                self.client_socket = None
                time.sleep(2)  # Wait before reconnecting

    def __del__(self):
        """Clean up socket on object destruction."""
        if self.client_socket:
            self.client_socket.close()

if __name__ == "__main__":
    consumer = KafkaConsumer()
    consumer.read()