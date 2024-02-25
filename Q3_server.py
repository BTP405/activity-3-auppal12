import socket
import threading
from pickling import unpickle_data, pickle_data

# Function to handle incoming connections from clients
def handle_client(client_socket, address):
    try:
        # Get the client ID
        client_id = clients.index(client_socket) + 1

        while True:
            # Receive pickled message from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Unpickle the message
            message = unpickle_data(data)

            # Display the message on the server with client ID
            print(f"Client {client_id}: {message}")

            # Check if the client wants to exit
            if message.lower() == "exit":
                print(f"Client {client_id} has left.")
                break

    except ConnectionResetError:
        # Handle the case where the client forcibly closed the connection
        print(f"Client {client_id} has left.")
    except Exception as e:
        print(f"Error handling client {address}: {e}")

    finally:
        # Remove the client from the list and close the socket
        lock.acquire()
        try:
            clients.remove(client_socket)
        finally:
            lock.release()
        client_socket.close()


# Function to broadcast a message to all connected clients
def broadcast(message, sender_socket):
    lock.acquire()
    try:
        for client in clients:
            # Send the pickled message to all clients except the sender
            if client != sender_socket:
                client.send(pickle_data(message))
    finally:
        lock.release()

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)

    print("Server is listening on port 5555...")

    while True:
        client_socket, address = server.accept()

        # Add the new client to the list
        lock.acquire()
        try:
            clients.append(client_socket)
        finally:
            lock.release()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# List to keep track of connected clients
clients = []

# Lock for synchronization
lock = threading.Lock()

if __name__ == "__main__":
    main()
