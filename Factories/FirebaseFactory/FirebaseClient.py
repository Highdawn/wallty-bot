import configparser
from firebase import firebase


class FirebaseClient:
    collection = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.configs')
        self.client = firebase.FirebaseApplication(config["FIREBASE"]["Url"], None)

    def get(self):
        return self.client.get(self.collection, None)

    def get_by_doc_id(self, doc_id):
        return self.client.get(self.collection, doc_id)

    def create(self, data):
        return self.client.post(self.collection, data)

    def update(self, doc_id, data):
        return self.client.put(self.collection, doc_id, data)

    def delete(self, doc_id):
        return self.client.delete(self.collection, doc_id)
