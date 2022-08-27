import pickle

def loadFile():
    filename = input("Input back up file name: ")
    try:
        with open(f"{filename}.pkl", 'rb') as f:
            file = pickle.load(f)
        return file
    except FileNotFoundError:
        return {}