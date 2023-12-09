import pygame
import Warehouse

class Player:
    def __init__(self, player_name, player_at_back, target_inventory=20, regime_native=False, stress_mod_for_turn = 0.05, use_stress = True):
        self.player_name = player_name# имя игрока
        self.lack_of_goods = 0# долг по поставке
        self.penalty = 0# цена за просрочку/хранение
        
        self.regime_native = regime_native#какая логика создания заказов
        
        self.warehouse_stock = Warehouse()# склад игрока (Square)
        
        self.player_at_back = player_at_back#наш поставщик
        
        self.order_in_front = Warehouse()# заказ игроку (Square)
        self.order_at_back = Warehouse()# заказ игрока (Square)
        
        
        self.warehouse_in_front = Warehouse()# промежуточное поле перед игроком (Square)
        self.warehouse_at_back = Warehouse()# промежуточное поле после игрока (Square)
        self.target_inventory = target_inventory#к какому запасу на складе стремится
        
        self.stress_ = 1
        self.stress_mod_for_turn = stress_mod_for_turn
        self.use_stress = use_stress
    def make_order(self):
        # Расчет заказа
        if self.regime_native:
            #наивноe решениe
            self.order_at_back.number = max(int((self.order_in_front.number + self.warehouse_in_front.number + self.target_inventory - self.warehouse_stock.number)*self.stress_), 0)
        else:
            self.order_at_back.number = max(int((self.order_in_front.number + (self.target_inventory - self.warehouse_stock.number + self.order_in_front.number * 4))*self.stress_), 0)

            
            
    def ship_order(self, requested_amount):
        #отгружаем груз (склад - б2) (отобразить)
        shipment = min(requested_amount+self.lack_of_goods, self.warehouse_stock.number)#объем поставки
        self.warehouse_in_front.number =  shipment
        self.warehouse_stock.number -= shipment
        
        #считаем долг
        self.lack_of_goods += (requested_amount-shipment)
        if self.use_stress:
            if self.lack_of_goods > 0:
                self.increase_stress()
            else:
                self.decrease_stress()
        return(shipment)
    def refill_player_warehouse(self, received_goods):
        # получаем груз от игрока далее (б1 - склад) (отобразить)
        self.warehouse_stock.number += received_goods
        #принимаем товар от игрока далее на промежуточную точку (б2 - б1) (отобразить)
        if self.player_at_back is not None:
            self.warehouse_at_back.number = self.player_at_back.warehouse_in_front.number
        
    def step(self):
        
        self.refill_player_warehouse(self.warehouse_at_back.number)
        self.ship_order(self.order_in_front.number)
        
        self.penalty += (self.lack_of_goods*2 + self.warehouse_stock.number)
        #передаем заказы далее (разместить - входящий) (отобразить)
        if self.player_at_back is not None:
            self.player_at_back.order_in_front.number = self.order_at_back.number 
            
        self.make_order()
    
    def increase_stress(self):
        if self.stress_<1.5:
            self.stress_ += self.stress_mod_for_turn
    def decrease_stress(self):
        if self.stress_>0.5:
            self.stress_ -= self.stress_mod_for_turn
    
    #псевдографика для тестирования
    def print_orders(self):
        print(self.order_in_front.number, '-', self.player_name,'-',self.order_at_back.number, '|', end='')
    def print_warehouse(self):
        print(self.warehouse_in_front.number, '-+', self.warehouse_stock.number,'d:',self.lack_of_goods,'+-',self.warehouse_at_back.number,'|', end='')
