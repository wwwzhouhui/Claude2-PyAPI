import pickle

class idStore():
    def __init__(self):
        self.id = None

    def get_id(self):
        if self.id is None:
            try:
                with open('id.pickle', 'rb') as f:
                    self.id = pickle.load(f)
            except FileNotFoundError:
                print("No ID found. Creating new ID")
        return self.id

    def set_id(self,id):
        self.id = id
        with open('id.pickle', 'wb') as f:
            pickle.dump(self.id, f)