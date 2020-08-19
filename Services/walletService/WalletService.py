from Services.firebaseService.FirebaseClient import FirebaseClient
from Tools.DictionaryHandler import query_dictionary

collection = "wallets"


def get_by_creator(creator_id):
    documents = get()
    return query_dictionary(documents, {"creator": creator_id})


def get():
    client = FirebaseClient()
    return client.get(collection)


def create(start_balance, message_from):
    data = {
        "balance": start_balance,
        "creator": message_from
    }
    client = FirebaseClient()
    return client.create(collection, data)


def update(doc_id, balance, message_from):
    data = {
        "balance": balance,
        "creator": message_from
    }
    client = FirebaseClient()
    return client.update(collection, doc_id, data)


def delete(doc_id):
    client = FirebaseClient()
    return client.delete(collection, doc_id)
