from datetime import datetime

class Message:
    def __init__(self, messageid: int, userid: int, chatid: int, date: int, text: str) -> None:
        self.messageid = messageid
        self.userid = userid
        self.chatid = chatid
        self.date = date
        self.text = text
    def __str__(self) -> str:
        return "[G{}][U-{}] {} {}: {}".format(
            self.chatid,
            self.userid,
            datetime.utcfromtimestamp(self.date).strftime('%Y-%m-%d %H:%M:%S'),
            self.userid,
            self.text
        )

class PriceInfo:
    def __init__(self, price: float, bnb_price: float, symbol: str, name: str) -> None:
        self.price = price
        self.bnb_price = bnb_price
        self.symbol = symbol
        self.name = name
    
    def __str__(self) -> str:
        return "{} {}-BNB={:.6f} {}-USD={:.4f}".format(
            self.name,
            self.symbol, self.bnb_price,
            self.symbol, self.price
        )
