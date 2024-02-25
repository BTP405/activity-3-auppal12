import socket
from pickling import pickle_data, unpickle_data
import threading

def start_worker(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Worker listening for tasks...")
    
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_task, args=(client_socket,)).start()

def handle_task(client_socket):
    task_data = client_socket.recv(4096)
    task = unpickle_data(task_data)
    result = execute_task(task)
    
    # Pickle the result data without saving to a file
    result_data = pickle_data(result)
    
    client_socket.send(result_data)
    client_socket.close()

def execute_task(task):
    # Execute the task
    function, args, kwargs = task
    result = function(*args, **kwargs)
    return result

if __name__ == "__main__":
    start_worker("localhost", 5000)
