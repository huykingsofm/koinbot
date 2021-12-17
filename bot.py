import threading
from api import API
from router import BotRouter
from services import OrderService

class Bot:
    def __init__(self) -> None:
        self.__stop_bot = OrderService()
        t = threading.Thread(target=self.__stop_bot.serve)
        t.start()
    
    def serve(self):
        while True:
            message = API.getMessage()
            if not message:
                continue

            handler = BotRouter.route(message)
            handler.respond()
        