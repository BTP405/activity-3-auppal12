import socket
import threading
from pickling import pickle_data, unpickle_data

# Function to receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            # Receive pickled message from the server
            data = client_socket.recv(1024)
            if not data:
                break

            # Unpickle the message and print it
            message = unpickle_data(data)
            print(message)

    except ConnectionAbortedError:
        print("The connection was aborted by the server.")
    except ConnectionResetError:
        print("The connection was reset by the server.")
    except Exception as e:
        print(f"Error receiving messages: {e}")

    finally:
        # Close the client socket
        client_socket.close()

# Main function to start the client
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        while True:
            # Get user input and send it to the server after pickling
            message = input("Enter your message or enter \"exit\" to close the chat: ")

            # Check if the user wants to exit
            if message.lower() == "exit":
                print("Closing the client...")
                break

            client.send(pickle_data(message))

    except KeyboardInterrupt: # Ctrl+C
        print("Closing the client...")

    finally:
        client.close()

if __name__ == "__main__":
    main()
