from Factories.ServicesFactory.ServicesFactory import ServicesFactory
from Repositories.walletFirebaseRepository.WalletFirebaseRepository import WalletFirebaseRepository
from Tools.DictionaryHandler import query_dictionary


class WalletService(ServicesFactory):

    def __init__(self):
        super().__init__(WalletFirebaseRepository())

    def get(self):
        return self.repository.get()

    def get_by_creator(self, creator_id):
        return query_dictionary(self.repository.get(), {"creator": creator_id})

    def create(self, start_balance, message_from):
        data = {
            "balance": start_balance,
            "creator": message_from
        }
        return self.repository.create(data)

    def update(self, doc_id, balance, message_from):
        data = {
            "balance": balance,
            "creator": message_from
        }
        return self.repository.update(doc_id, data)

    def delete(self, doc_id):
        return self.repository.delete(doc_id)
