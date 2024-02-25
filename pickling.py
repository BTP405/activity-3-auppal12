import pickle

def pickle_data(data, file_path=None):
    pickled_data = pickle.dumps(data)

    if file_path:
        with open(file_path, 'wb') as output_file:
            output_file.write(pickled_data)
    else:
        return pickled_data

def unpickle_data(pickled_data):
    return pickle.loads(pickled_data)
