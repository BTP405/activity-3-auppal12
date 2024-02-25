import socket
import os
from pickling import unpickle_data

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Server is listening for incoming connections... ")

    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()

        try:
            print("Connected to: ", client_address)

            # Receive pickled file data
            pickled_data = client_socket.recv(1024)
            if not pickled_data:
                break

            # Unpickle the file data
            file_data = unpickle_data(pickled_data)

            # Specify the output file path
            output_file_path = os.path.join('C:/Users/amito/Desktop', 'received_file.txt')

            # Save the unpickled data to a file (if needed)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)

            print("File received and saved to:", output_file_path)

        finally:
            # Close the connection
            client_socket.close()

if __name__ == "__main__":
    run_server()