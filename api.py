import os
import interfaces
from contract import Contract

import json
import requests

class API:
    __token = os.environ['BOTOKEN']
    __tele_url = "https://api.telegram.org/bot{}/{}".format(__token, "{}")
    __pancake_url = "https://api.pancakeswap.info/api/v2/tokens/{}"
    __latest_update = 0
    
    @staticmethod
    def getMessage() -> interfaces.Message:
        params = {}
        params["offset"] = API.__latest_update
        params["limit"] = 1
        params["timeout"] = 3
        update = requests.get(API.__tele_url.format("getUpdates"), params=params)
        if update.status_code != 200:
            print(update.content.decode())
            return None
        
        update = json.loads(update.content.decode())
        if not update["ok"]:
            print(update.content.decode())
            return None
        
        if len(update["result"]) == 0:
            return None

        API.__latest_update = update["result"][0]["update_id"] + 1
    
        try:
            message = update["result"][0]["message"]
            message["text"]
        except KeyError:
            return None
    
        return interfaces.Message(message["message_id"], message["from"]["id"],
            message["chat"]["id"], message["date"], message["text"])

    @staticmethod
    def sendMessage(message: str, rep_to: interfaces.Message) -> bool:
        params = {}
        params["reply_to_message_id"] = rep_to.messageid
        params["chat_id"] = rep_to.chatid
        params["text"] = message
        result = requests.get(API.__tele_url.format("sendMessage"), params=params)
        if result.status_code != 200:
            print(result.content.decode())
            return False
        
        result = json.loads(result.content.decode())
        if result["ok"]:
            print("{} -> {}".format(rep_to, message))
        else:
            print("sendMsg Err: {}".format(result))

        return result["ok"]

    @staticmethod
    def getPrice(contract=Contract.STARS) -> interfaces.PriceInfo:
        info = requests.get(API.__pancake_url.format(contract))
        if info.status_code != 200:
            print(info.content.decode())
            return None

        info = json.loads(info.content.decode())["data"]
        return interfaces.PriceInfo(float(info["price"]), float(info["price_BNB"]),
            info["symbol"], info["name"])
