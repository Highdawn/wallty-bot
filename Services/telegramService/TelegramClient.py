import configparser
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class TelegramClient:

    previous_command = None

    def __init__(self):
        self.previous_command = None
        config = configparser.ConfigParser()
        config.read('.configs')
        self.client = telepot.Bot(config["TELEGRAM"]["BotToken"])

    def start_listening(self, handler):
        MessageLoop(self.client, handler).run_as_thread()

    def send_message(self, chat_id, message, markup=None):
        self.client.sendMessage(chat_id, message, reply_markup=markup)

    def delete_message(self, chat_id, message_id):
        self.client.deleteMessage((chat_id, message_id))

        # if msg.get('data'): # Checks if is a inline response
        #     command = msg['data'].split("_")
        #     self.client.deleteMessage((msg['message']['chat']['id'], msg['message']['message_id']))
        # elif msg.get('text'): # Checks if is a text response
        #     command = msg['text'].split("_")
        #     if command[0] != '/start':
        #         self.client.deleteMessage((msg['chat']['id'], msg['message_id']))
        # else:
        #     print("Unable to obtain clear message")
        # self.message = command