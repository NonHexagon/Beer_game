import pygame
import sys
from random import *
from Player import Player
from Warehouse import Warehouse
from pygame.locals import *
import pandas as pd


class Game:
    def __init__(self):
        self.players = []
        self.demand_data = None
        use_draw = True
        self.w = 1200
        self.h = 800
        
    def load_demand_data(self, file_path):
        # Загрузка данных о спросе из файла Excel (0-ой столбик)
        self.demand_data = pd.read_excel(file_path)

    def add_player(self, player_name, order_at_back=0, target_inventory=20, regime_native=False,
                   stress_mod_for_turn=0.05, use_stress=True, 
                   h=20, w = 75, w_ot=10, h_ot=5, letter='B'
                  ):
        if len(self.players) == 0:
            player_at_back = None
            letter='П'
        else:
            player_at_back = self.players[0]

        # Добавление игрока
        player = Player(player_name, player_at_back, h, w, w_ot, h_ot,
                        target_inventory, regime_native, stress_mod_for_turn, use_stress,
                         letter=letter)
        player.refill_player_warehouse(20)
        player.order_in_front.number = self.demand_data.iloc[0, 0]
        self.players.insert(0, player)

    def run_game(self, num_rounds):
        
        pygame.init()
        
        
        screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Beer Game')
        # Определение шрифта
        font = pygame.font.Font(None, 20)
        # Главный цикл игры
        running = True
        while running:     
            # Запуск игры
            for rounds in range(num_rounds):
                # Обработка событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
                # Очистка экрана
                screen.fill((255, 255, 255))
            
                self.players[0].order_in_front.number = self.demand_data.iloc[
                    rounds, 0]  # Получение внешнего спроса из данных
                i=0
                for player in self.players:
                    player.step(screen, font)
                    text = font.render(player.player_name+': штраф: '+str(player.penalty), True, (0, 0, 0))
                    
                    rect = pygame.math.Vector2((20,60*i))
                    screen.blit(text, rect)
                    i+=1
                #player.save_history()

                pygame.time.delay(1000*3)  # Задержка в 5 секунду
                # Обновление экрана
                pygame.display.flip()
            break
        # Завершение работы Pygame
        pygame.quit()  # Выход из Pygame после завершения цикла      

        
    def main(self, players_list, file_path, stress_mod_for_turn, target_inventory, use_stress, regime_native):
        self.load_demand_data(file_path)
        sh=len(players_list)
        w=int(self.w/(sh+1))
        sh=sh+0.2#1.5
        for i in range (len(players_list)):
            self.add_player(players_list[i], w = int(w*(sh-i)),w_ot=w, h = self.h//2, h_ot=self.h//6, stress_mod_for_turn=float(stress_mod_for_turn[i]), target_inventory=int(target_inventory[i]),use_stress=use_stress, regime_native=regime_native)# order_at_back=0, 20, False, True, h=20, w = 75, w_ot=10, h_ot=5, letter='B
            #print('lll', int(w*(sh-i*2)))
        self.run_game(self.demand_data.shape[0])

#, _box.text.split('; '), , )
if __name__ == "__main__":
    game = Game()
    game.main(['manufacturer', 'distributor', 'wholesaler', 'retailer'], 'demand_data.xlsx')
#print(size, w+w_ot,w, w-w_ot, h, h+h_ot)
