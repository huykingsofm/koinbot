import random

from api import API
from interfaces import Message
from contract import ContractDict
from services import Order, OrderService, OrderType


class DefaultBot:
    __INVALID_MSG__ = [
        "Sai lệnh rồi ba",
        "Mé, viết sai rồi",
        "Vãi l*n, lệnh tầm bậy",
        "Alo alo, nhìn lệnh chướng vl",
        "Lệnh xàm vãi c*c",
        "Ghi cái qq gì thế man"
    ]

    def __init__(self, message: str, reply_to: Message) -> None:
        self._argv = message.split()
        self._reply_to = reply_to
        
    def parse_argv(self) -> bool:
        return True
    
    def _default_handle(self) -> bool:
        invalid_command = random.choice(DefaultBot.__INVALID_MSG__)
        msg = "{}, gõ /help đi".format(invalid_command)
        return API.sendMessage(msg, self._reply_to)

    def handle(self) -> bool:
        return self._default_handle()

    def respond(self):
        if self.parse_argv() == False:
            return self._default_handle()
        
        return self.handle()


class HelpBot(DefaultBot):
    __HELPER__ = "/hi - Chào bot đi bạn, bot sẽ yêu bạn\n" \
                 "/order token price [(high)|low] - Đặt lệnh thông báo khi giá vượt giới hạn\n" \
                 "/say - Nói gì đi bot"

    def parse_argv(self) -> bool:
        return len(self._argv) == 1

    def handle(self) ->bool:
        return API.sendMessage(HelpBot.__HELPER__, self._reply_to)

class HelloBot(DefaultBot):
    def parse_argv(self) -> bool:
        return len(self._argv) == 1
    
    def handle(self) -> bool:
        return API.sendMessage("https://www.youtube.com/watch?v=NmH2Ijv076Q", self._reply_to)


class OrderBot(DefaultBot):
    def parse_argv(self) -> bool:
        if len(self._argv) != 3 and len(self._argv) != 4:
            return False

        self.stop_type = OrderType.HIGH
        self.token = self._argv[1].upper()
        try:
            self.price = float(self._argv[2])
        except ValueError:
            return False
        
        if len(self._argv) == 4:
            if self._argv[1] != "low" and self._argv[3] != "high":
                return False
            self.stop_type = OrderType.HIGH if self._argv[3] == "high" else OrderType.LOW
            
        return True

    def handle(self) -> bool:
        id = OrderService.push_order(Order(self.token, self.stop_type, self.price, self._reply_to))
        API.sendMessage("Successfully. Please check [Order-{}] in the future".format(id), self._reply_to)


class RandomBot(DefaultBot):
    __SOMETHING__ = [
        "Vãi l*n đòi nói chuyện với bot, đi kiếm người yêu đi ba",
        "https://www.youtube.com/watch?v=NmH2Ijv076Q",
        "https://www.youtube.com/watch?v=4slQkoipQvk",
        "Sống trong đời sống, cần có một tấm lòn",
        "Lạ lòn em hỡi, ....",
        "Stars to the hell",
        "Bot cũng biết mệt, cho nghỉ xíu đi",
        "Ai cho xin server xịn hơn đê, máy chịu hết nổi rồi"
    ]
    
    def handle(self) -> bool:
        return API.sendMessage(random.choice(RandomBot.__SOMETHING__), self._reply_to)

class PriceBot(DefaultBot):
    def parse_argv(self) -> bool:
        if len(self._argv) != 2:
            return False
        
        self.token = self._argv[1].upper()

        return True

    def handle(self) -> bool:
        try:
            contract = ContractDict[self.token]
        except KeyError:
            return API.sendMessage("Éo chơi đồng này, OK!", self._reply_to)

        priceInfo = API.getPrice(contract)

        if priceInfo == None:
            return API.sendMessage("Đồng éo gì đây bạn??", self._reply_to)

        msg = "{} {}/BNB={}  {}/USD={}".format(
            priceInfo.name,
            priceInfo.symbol, priceInfo.bnb_price,
            priceInfo.symbol, priceInfo.price)

        return API.sendMessage(msg, self._reply_to)
