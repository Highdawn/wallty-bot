import configparser
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class TelegramClient:
    previous_commands = {}

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.configs')
        self.client = telepot.Bot(config["TELEGRAM"]["BotToken"])

    def start_bot(self):
        self.start_listening(self.message_handler)
        while True:
            pass

    def start_listening(self, handler):
        MessageLoop(self.client, handler).run_as_thread()

    def send_message(self, chat_id, message, markup=None):
        self.client.sendMessage(chat_id, message, reply_markup=markup)

    def delete_message(self, chat_id, message_id):
        self.client.deleteMessage((chat_id, message_id))

    @staticmethod
    def message_handler(msg):
        print(msg)

    @staticmethod
    def create_button(text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    @staticmethod
    def create_markup(buttons):
        return InlineKeyboardMarkup(inline_keyboard=buttons)
