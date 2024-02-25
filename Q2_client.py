import socket
from pickling import pickle_data, unpickle_data
from Q2_tasks import add

def send_task(host, port, task):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        # Pickle the task data without saving to a file
        task_data = pickle_data(task)
        
        client_socket.sendall(task_data)
        result_data = client_socket.recv(4096)
        
        # Unpickle the result data
        result = unpickle_data(result_data)
        
        return result

if __name__ == "__main__":
    # Now, use the imported function from tasks.py
    add_task = (add, (3, 4), {})
    
    # Send task to the worker
    result = send_task("localhost", 5000, add_task)
    
    print("Result:", result)
