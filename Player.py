import pygame
from Warehouse import Warehouse  # рубрика учимся правильно импортировать


class Player:
    def __init__(self, player_name, player_at_back, 
                 h = 10, w = 10, w_ot=3, h_ot=3, 
                 target_inventory=20, regime_native=False, stress_mod_for_turn=0.05,
                 use_stress=True, use_draw=True, letter='B'
                 ):

       
        self.history={'penalties':[], 'order_in_front':[], 'warehouse_in':[], 'lack_of_goods':[], 'warehouse_states':[], 'warehouse_at_back':[], 'order_at_back':[]}

        self.player_name = player_name  # имя игрока
        self.lack_of_goods = 0  # долг по поставке
        self.penalty = 0  # цена за просрочку/хранение
        self.regime_native = regime_native  # какая логика создания заказов
        
        
        
        self.player_at_back = player_at_back  # наш поставщик
        
        size=max(min(int(w_ot//3), int(h_ot//3)), 1)
        w_ot=w_ot//4
        self.order_in_front = Warehouse(title='Входящий заказ', size=size, color=(255, 255, 0), x=w-w_ot, y=h+h_ot)  # заказ игроку (Square)
        self.order_at_back = Warehouse(title='Исходящий заказ', size=size, color=(255, 255, 0), x=w+w_ot, y=h+h_ot)  # заказ игрока (Square)
        #print(size, w+w_ot,w, w-w_ot, h, h+h_ot)
        h=h-h_ot
        self.warehouse_in_front = Warehouse(title=letter+'2', size=size, color=(255, 0, 255), x=w-w_ot, y=h)  # промежуточное поле перед игроком (Square)
        self.warehouse_stock = Warehouse(title=player_name, size=size, color=(255, 0, 255), x=w, y=h)  # склад игрока (Square)
        self.warehouse_at_back = Warehouse(title=letter+'1', size=size, color=(255, 0, 255), x=w+w_ot, y=h)  # промежуточное поле после игрока (Square)
        
        
        self.target_inventory = target_inventory  # к какому запасу на складе стремится
        self.stress_ = 1
        self.stress_mod_for_turn = stress_mod_for_turn
        self.use_stress = use_stress
        self.use_draw = use_draw
        
        self.save_history()

    def make_order(self):
        # Расчет заказа
        if self.regime_native:
            # наивноe решениe
            self.order_at_back.number = max(int((
                self.order_in_front.number + self.warehouse_in_front.number + self.target_inventory
                - self.warehouse_stock.number) * self.stress_),
                0)
        else:
            self.order_at_back.number = max(int((self.order_in_front.number + (
                 self.target_inventory - self.warehouse_stock.number + self.order_in_front.number * 4)) * self.stress_),
                0)

    def ship_order(self, requested_amount):
        # отгружаем груз (склад - б2) (отобразить)
        shipment = min(requested_amount + self.lack_of_goods, self.warehouse_stock.number)  # объем поставки
        self.warehouse_in_front.number = shipment
        self.warehouse_stock.number -= shipment
        # считаем долг
        self.lack_of_goods += (requested_amount - shipment)
        
        # передаем заказы далее (разместить - входящий) (отобразить)
        if self.player_at_back is not None:
            self.player_at_back.order_in_front.number = self.order_at_back.number
        else:
            self.warehouse_at_back.number = self.order_at_back.number
        #return shipment

    def refill_player_warehouse(self, received_goods):
        # получаем груз от игрока далее (б1 - склад) (отобразить)
        self.warehouse_stock.number += received_goods
        # принимаем товар от игрока далее на промежуточную точку (б2 - б1) (отобразить)
        if self.player_at_back is not None:
            self.warehouse_at_back.number = self.player_at_back.warehouse_in_front.number

    def calc_penalty(self):
        if self.use_stress:
            if self.lack_of_goods > 0:
                self.increase_stress()
            else:
                self.decrease_stress()
        
        self.penalty += (self.lack_of_goods * 2 + self.warehouse_stock.number)
        
    def step(self, screen=None, font=None):
        self.refill_player_warehouse(self.warehouse_at_back.number)
        self.ship_order(self.order_in_front.number)
        
        self.calc_penalty()
        
            
        self.make_order()
        
        self.save_history()
        
        if self.use_draw:
            self.draw(screen, font)
    
    def draw(self, screen, font):
        #print(2)
        self.order_in_front.draw(screen, font)
        self.order_at_back.draw(screen, font)
        
        self.warehouse_in_front.draw(screen, font)
        self.warehouse_stock.draw(screen, font, self.lack_of_goods)
        self.warehouse_at_back.draw(screen, font)
    
    
    def increase_stress(self):
        if self.stress_ < 1.5:
            self.stress_ += self.stress_mod_for_turn

    def decrease_stress(self):
        if self.stress_ > 0.5:
            self.stress_ -= self.stress_mod_for_turn

    # псевдографика для тестирования
    def print_orders(self):
        print(self.order_in_front.number, '-', self.player_name, '-', self.order_at_back.number, '|', end='')

    def print_warehouse(self):
        print(self.warehouse_in_front.number, '-+', self.warehouse_stock.number, 'd:', self.lack_of_goods, '+-',
              self.warehouse_at_back.number, '|', end='')

    def save_history(self):
        self.history['penalties'].append(self.penalty)
        self.history['order_in_front'].append(self.order_in_front.number)
        self.history['warehouse_in'].append(self.warehouse_in_front.number)
        self.history['lack_of_goods'].append(self.lack_of_goods)
        self.history['warehouse_states'].append(self.warehouse_stock.number)
        self.history['warehouse_at_back'].append(self.warehouse_at_back.number)
        self.history['order_at_back'].append(self.order_at_back.number)
        

        
        

