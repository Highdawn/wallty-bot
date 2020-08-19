import configparser
from firebase import firebase


class FirebaseClient:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.configs')
        self.client = firebase.FirebaseApplication(config["FIREBASE"]["Url"], None)

    def get(self, collection):
        return self.client.get(collection, None)

    def get_by_doc_id(self, collection, doc_id):
        return self.client.get(collection, doc_id)

    def create(self, collection, data):
        return self.client.post(collection, data)

    def update(self, collection, doc_id, data):
        return self.client.put(collection, doc_id, data)

    def delete(self, collection, doc_id):
        return self.client.delete(collection, doc_id)
