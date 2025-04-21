import socket

class KafkaProducer:
    def __init__(self, host="localhost", port=9092):
        self.host = host
        self.port = port

    def add(self, message):
        """Send a message to the broker."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.host, self.port))
            client_socket.send(f"PRODUCE {message}".encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8").strip()
            print(f"Broker response: {response}")
        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    producer = KafkaProducer()
    while True:
        message = input("What do you want to add? (type 'exit' to quit): ")
        if message.lower() == "exit":
            break
        producer.add(message)