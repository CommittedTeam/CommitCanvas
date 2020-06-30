"""Code to interact with pickle file."""
# pylint: disable=import-error
import pickle


def write_to_pickle(path, data):
    """Write objects to the pickle file."""
    # Add the new object to the file, and don't replace the existing data
    with open(path, "ab") as file:
        bin_obj = pickle.dumps(data)
        file.write(bin_obj)


def read_from_pickle(path):
    """Read objects from the pickle file."""
    # Read multiple objects from the file
    with open(path, "rb") as file:
        while True:
            try:
                print(pickle.load(file))
            except EOFError:
                break
