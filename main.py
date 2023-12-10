import pygame
import sys
from random import *
from Player import Player
from Warehouse import Warehouse
import pandas as pd


class Game:
    def __init__(self):
        self.players = []
        self.demand_data = None

    def load_demand_data(self, file_path):
        # Загрузка данных о спросе из файла Excel (0-ой столбик)
        self.demand_data = pd.read_excel(file_path)

    def add_player(self, player_name, order_at_back=0, target_inventory=20, regime_native=False,
                   stress_mod_for_turn=0.05, use_stress=True):
        if len(self.players) == 0:
            player_at_back = None
        else:
            player_at_back = self.players[0]

        # Добавление игрока
        player = Player(player_name, player_at_back,
                        target_inventory, regime_native, stress_mod_for_turn, use_stress)
        player.refill_player_warehouse(20)
        player.order_in_front.number = self.demand_data.iloc[0, 0]
        self.players.insert(0, player)

    def run_game(self, num_rounds):
        # Запуск игры
        for rounds in range(num_rounds):
            self.players[0].order_in_front.number = self.demand_data.iloc[
                rounds, 0]  # Получение внешнего спроса из данных
            for player in self.players:
                player.step()

            self.players[-1].warehouse_at_back.number = self.players[-1].order_at_back.number
        for player in self.players:
            print(player.penalty)


game = Game()
game.load_demand_data('demand_data.xlsx')
game.add_player('manufacturer')
game.add_player('distributor')
game.add_player('wholesaler')
game.add_player('retailer')
game.run_game(50)
