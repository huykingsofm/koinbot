import interfaces
from api import API
from contract import ContractDict

import time
import threading
from enum import Enum
from typing import Dict

class OrderType(Enum):
    HIGH = 0
    LOW = 1

class Order:
    def __init__(self, token: str, type: OrderType, price: float, requirer: interfaces.Message) -> None:
        self.token = token
        self.type = type
        self.price = price
        self.requirer = requirer

class OrderService:
    __orders: Dict[int, Order] = {}
    __latest_id = 0
    __orders_lock = threading.Lock()

    @staticmethod
    def push_order(order: Order):
        OrderService.__orders_lock.acquire()
        OrderService.__latest_id += 1
        OrderService.__orders[OrderService.__latest_id] = order
        OrderService.__orders_lock.release()

        return OrderService.__latest_id

    @staticmethod
    def serve_once():
        OrderService.__orders_lock.acquire()
        removed_id = []
        for id, order in OrderService.__orders.items():
            try:
                priceInfo = API.getPrice(contract=ContractDict[order.token])
            except KeyError:
                priceInfo = None
            
            msg = None
            
            if not priceInfo:
                msg = "[Order-{}] Not support {} token".format(id, order.token)
                
            elif order.type == OrderType.HIGH and priceInfo.price >= order.price:
                msg = "[Order-{}][NOTIFICATION] {}'s price is higher {}".format(id, order.token, order.price)

            elif order.type == OrderType.LOW and priceInfo.price <= order.price:
                msg = "[Order-{}][NOTIFICATION] {}'s price is lower {}".format(id, order.token, order.price)
                
            if msg:
                API.sendMessage(msg, order.requirer)
                removed_id.append(id)

        for id in removed_id:
            OrderService.__orders.pop(id)

        OrderService.__orders_lock.release()

    @staticmethod
    def serve():
        while True:
            time.sleep(20)
            OrderService.serve_once()
