import socket
from pickling import pickle_data

def get_file_path_from_user():
    """Get the file path from the user and return it.
    If the file does not exist, keep asking for the file path until a valid file is entered."""

    while True:
        file_path = input("Enter the path of the file to send: ")
        try:
            with open(file_path, 'rb'):
                return file_path
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")

def run_client():

    file_path = get_file_path_from_user()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    try:
        # Read the file content
        with open(file_path, 'rb') as file:
            data = file.read()

        # Pickle the file data without saving to a file
        pickled_data = pickle_data(data)

        # Send the pickled file data to the server
        client_socket.sendall(pickled_data)

        print("File sent to the server.")

    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()