import pygame
import sys
from random import *
from Player import Player
import Warehouse


class Game:
    def __init__(self):
        pass


valera = Player(role='vendor')
nikita = Player(role='wholesaler')
kirill = Player(role='factory')
oleg = Player(role='seller')
crowd = Player(role='customer')

kirill.refill_warehouse(5)
nikita.refill_warehouse(5)
valera.refill_warehouse(5)
oleg.refill_warehouse(5)

easy_start = [1, 3, 3, 2, 2]
cold_start = [20] * 2
easy_out = [6] * 23

easy_start.extend(cold_start)
easy_start.extend(easy_out)

print(easy_start)

for index, week in enumerate(easy_start):
    order_for_seller = crowd.make_order(week)
    order_for_wholesaler = oleg.make_order(week + oleg.stress_)
    order_for_vendor = nikita.make_order(week + nikita.stress_)
    order_for_factory = valera.make_order(week + valera.stress_)
    if week % 2 == 0:
        shipped_order_by_seller = oleg.ship_order(order_for_seller)
        shipped_order_by_wholesaler = nikita.ship_order(order_for_wholesaler)
        shipped_order_by_vendor = valera.ship_order(order_for_vendor)
        shipped_order_by_factory = kirill.ship_order(order_for_factory)

        if index % 2 == 0:
            crowd.refill_warehouse(shipped_order_by_seller)
            oleg.refill_warehouse(shipped_order_by_wholesaler)
            nikita.refill_warehouse(shipped_order_by_vendor)
            valera.refill_warehouse(shipped_order_by_factory)
            kirill.refill_warehouse(week + oleg.stress_)


print(f'{crowd.warehouse_stock}')
print(f'{oleg.warehouse_stock, oleg.stress_, oleg.lack_of_goods}')
print(f'{nikita.warehouse_stock, nikita.stress_, nikita.lack_of_goods}')
print(f'{valera.warehouse_stock, valera.stress_, valera.lack_of_goods}')
print(f'{kirill.warehouse_stock, kirill.stress_, kirill.lack_of_goods}')

