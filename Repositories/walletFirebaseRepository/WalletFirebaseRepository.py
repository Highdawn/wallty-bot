from Factories.FirebaseFactory.FirebaseClient import FirebaseClient


class WalletFirebaseRepository(FirebaseClient):

    def __init__(self):
        super().__init__()
        self.collection = "wallets"
