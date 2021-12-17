import subbot
from interfaces import Message

class BotRouter:
    @staticmethod
    def route(reply_to: Message):
        message = reply_to.text
        if message.startswith("/hi"):
            return subbot.HelloBot(message, reply_to)
        elif message.startswith("/help"):
            return subbot.HelpBot(message, reply_to)
        elif message.startswith("/order"):
            return subbot.OrderBot(message, reply_to)
        elif message.startswith("/say"):
            return subbot.RandomBot(message, reply_to)
        elif message.startswith("/price"):
            return subbot.PriceBot(message, reply_to)
        else:
            return subbot.DefaultBot(message, reply_to)
