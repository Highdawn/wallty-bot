from Factories.TelegramFactory.TelegramClient import TelegramClient
from Services.walletService.WalletService import WalletService


class WalletTelegramService(TelegramClient):

    def message_handler(self, msg):
        if 'message' in msg:
            chat_id = msg['message']['chat']['id']
            message_id = msg['message']['message_id']
            text = msg['data']
            message_from = msg['message']['from']['id']
        else:
            chat_id = msg['chat']['id']
            message_id = msg['message_id']
            text = msg['text']
            message_from = msg['from']['id']
        self.delete_message(chat_id, message_id)
        response = self.process_message(text, message_from)
        self.send_message(chat_id, response['message'], response['markup'])

    def process_message(self, text, message_from):
        text = text.lower()
        if self.previous_commands.get(message_from):
            user_previous_command = self.previous_commands[message_from]
        else:
            user_previous_command = None

        if user_previous_command == "add balance":
            self.previous_commands[message_from] = None
            text = text.replace(',', '.')
            value = self.validate_balance_value(text)
            if not value:
                return {
                    "message": "Invalid value",
                    "markup": None
                }
            wallet = WalletService().get_by_creator(message_from)
            if not wallet:
                return {
                    "message": "You don't have a wallet created",
                    "markup": None
                }
            wallet_id = list(wallet.keys())[0]
            new_balance = float(wallet[wallet_id]["balance"]) + value
            WalletService().update(wallet_id, new_balance, message_from)
            return {
                "message": "Wallet updated successfully, you currently have a balance of " + str(new_balance),
                "markup": None
            }

        if user_previous_command == "remove balance":
            self.previous_commands[message_from] = None
            text = text.replace(',', '.')
            value = self.validate_balance_value(text)
            if not value:
                return {
                    "message": "Invalid value",
                    "markup": None
                }

            wallet = WalletService().get_by_creator(message_from)
            if not wallet:
                return {
                    "message": "You don't have a wallet created",
                    "markup": None
                }
            wallet_id = list(wallet.keys())[0]
            new_balance = float(wallet[wallet_id]["balance"]) - value
            if new_balance < 0:
                return {
                    "message": "Unable to update wallet, value to remove is higher than the current balance, current "
                               "balance " + str(wallet[wallet_id]["balance"]),
                    "markup": None
                }
            WalletService().update(wallet_id, new_balance, message_from)

            return {
                "message": "Wallet updated successfully, you currently have a balance of " + str(new_balance),
                "markup": None
            }

        if user_previous_command == "delete wallet":
            self.previous_commands[message_from] = None
            WalletService().delete(text)
            return {
                "message": "Wallet deleted successfully",
                "markup": None
            }

        self.previous_commands[message_from] = text

        if text == "create wallet":
            created_wallet = WalletService().get_by_creator(message_from)
            if not created_wallet:
                response = WalletService().create(0, message_from)
                return {
                    "message": "ID of the wallet: " + response["name"],
                    "markup": None
                }
            else:
                return {
                    "message": "You already have a wallet created",
                    "markup": None
                }

        if text == "get wallet":
            created_wallet = WalletService().get_by_creator(message_from)
            if created_wallet:
                wallet_id = list(created_wallet.keys())[0]
                return {
                    "message": "ID of the wallet: " + wallet_id + "\nCurrent Balance: " + str(
                        created_wallet[wallet_id]["balance"]),
                    "markup": None
                }
            else:
                return {
                    "message": "You don't have a wallet created",
                    "markup": None
                }

        return self.get_response(text)

    def get_response(self, text):
        responses = {
            "options": {
                "message": "Greetings, what do you wish to do: ",
                "buttons": [
                    {"text": "Wallet", "callback_data": "options_wallet"},
                    {"text": "Movements", "callback_data": "options_movements"}
                ]
            },
            "help": {
                "message": self.get_available_commands(),
                "buttons": None
            },
            "/start": {
                "message": self.get_available_commands(),
                "buttons": None
            },
            "delete wallet": {
                "message": "Insert your wallet ID",
                "buttons": None
            },
            "update balance": {
                "message": "Select the type of update you want to do the balance",
                "buttons": [
                    {"text": "Add", "callback_data": "add balance"},
                    {"text": "Remove", "callback_data": "remove balance"}
                ]
            },
            "add balance": {
                "message": "Insert the value to add to the balance",
                "buttons": None
            },
            "remove balance": {
                "message": "Insert the value to remove from the balance",
                "buttons": None
            },
        }

        if text in responses:
            response = responses[text]
            buttons = []
            if response["buttons"] is not None:
                for button in response["buttons"]:
                    buttons.append([self.create_button(button["text"], button["callback_data"])])
                markup = self.create_markup(buttons)
            else:
                markup = None

            return {
                "message": response["message"],
                "markup": markup
            }
        else:
            return {
                "message": "Command not found",
                "markup": None
            }

    @staticmethod
    def validate_balance_value(text):
        try:
            value = float(text)
        except ValueError:
            return False
        if value < 0:
            return False
        return float(text)

    @staticmethod
    def get_available_commands():
        return "This are the current available commands: \n" \
               "help: Get list of commands \n" \
               "create wallet: Creates a new wallet \n" \
               "get wallet: Gets the balance  \n" \
               "delete wallet: Delete your wallet \n" \
               "add balance: Increase value of the wallet balance \n" \
               "remove balance: Decrease value of the wallet balance \n"
