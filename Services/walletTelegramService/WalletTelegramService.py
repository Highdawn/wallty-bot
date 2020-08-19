from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from Services.telegramService.TelegramClient import TelegramClient
from Services.walletService import WalletService

telegram_bot = TelegramClient()


def process_message(text, message_from, bot):
    print(bot.previous_command)
    print(text)

    if bot.previous_command == "add balance":
        bot.previous_command = None
        wallet = WalletService.get_by_creator(message_from)
        wallet_id = list(wallet.keys())[0]
        new_balance = int(wallet[wallet_id]["balance"]) + int(text)
        WalletService.update(wallet_id, new_balance, message_from)
        return {
            "message": "Wallet updated successfully, you currently have a balance of " + str(new_balance),
            "markup": None
        }

    if bot.previous_command == "remove balance":
        bot.previous_command = None
        wallet = WalletService.get_by_creator(message_from)
        wallet_id = list(wallet.keys())[0]
        new_balance = int(wallet[wallet_id]["balance"]) - int(text)
        if new_balance < 0:
            return {
                "message": "Unable to update wallet, value to remove is higher than the current balance, current "
                           "balance " + str(wallet[wallet_id]["balance"]),
                "markup": None
            }
        WalletService.update(wallet_id, new_balance, message_from)

        return {
            "message": "Wallet updated successfully, you currently have a balance of " + str(new_balance),
            "markup": None
        }

    if bot.previous_command == "delete wallet":
        bot.previous_command = None
        WalletService.delete(text)
        return {
            "message": "Wallet deleted successfully",
            "markup": None
        }

    bot.previous_command = text

    if text == "create wallet":
        created_wallet = WalletService.get_by_creator(message_from)
        if not created_wallet:
            response = WalletService.create(0, message_from)
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
        created_wallet = WalletService.get_by_creator(message_from)
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

    return get_response(text.lower())


def create_button(text, callback_data):
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def create_markup(buttons):
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_response(text):
    responses = {
        "options": {
            "message": "Greetings, what do you wish to do: ",
            "buttons": [
                {"text": "Wallet", "callback_data": "options_wallet"},
                {"text": "Movements", "callback_data": "options_movements"}
            ]
        },
        "help": {
            "message": "Sry mate cant help",
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
                buttons.append([create_button(button["text"], button["callback_data"])])
            markup = create_markup(buttons)
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


def start_bot():
    telegram_bot.start_listening(message_handler)
    while True:
        pass


def message_handler(msg):
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
    telegram_bot.delete_message(chat_id, message_id)
    response = process_message(text, message_from, telegram_bot)
    telegram_bot.send_message(chat_id, response['message'], response['markup'])
