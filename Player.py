import pygame


class Player:
    def __init__(self, role):
        self.role = role
        self.warehouse_stock = 0
        self.current_order = 0
        self.lack_of_goods = 0
        self.goods_sent = 0
        self.stress_ = 0

    def make_order(self, order_amount):
        self.current_order = order_amount + self.stress_
        return self.current_order

    def ship_order(self, requested_amount):
        if requested_amount + self.lack_of_goods <= self.warehouse_stock:
            self.warehouse_stock -= requested_amount
            return requested_amount
        else:
            self.lack_of_goods = requested_amount - self.warehouse_stock
            self.goods_sent = self.warehouse_stock
            self.warehouse_stock = 0
            self.increase_stress()
            return self.goods_sent

    def refill_warehouse(self, received_goods):
        if self.lack_of_goods == 0:
            self.warehouse_stock += received_goods

        elif self.lack_of_goods > received_goods:
            self.lack_of_goods -= received_goods
            self.decrease_stress()

        elif self.lack_of_goods < received_goods:
            received_goods -= self.lack_of_goods
            self.lack_of_goods = 0
            self.warehouse_stock = received_goods
            self.decrease_stress()

    def increase_stress(self):
        self.stress_ += 3

    def decrease_stress(self):
        if self.stress_ > 0:
            self.stress_ -= 1


