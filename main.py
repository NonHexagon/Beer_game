import pygame
from game import Game
# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 1000
HEIGHT = 800

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создание окна главного меню
menu_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")


use_stress = False
regime_native=False


font = pygame.font.Font(None, 36)
    
    
    
class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, start_text=""):
        super().__init__()
        self.color = (55, 255, 55)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = False
        self.text = start_text
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        #if self.backcolor:
        #    self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()
    
    
    
    
    
pygame.init()


clock = pygame.time.Clock()
text_input_box = TextInputBox(10,  HEIGHT / 2-100, 400, pygame.font.SysFont(None, 60), start_text="manufacturer; distributor; wholesaler; retailer")#WIDTH / 2,  HEIGHT / 2, 400, font)
players_list = pygame.sprite.Group(text_input_box)

xlsx_input_box = TextInputBox(10,  HEIGHT / 2+150, 400, pygame.font.SysFont(None, 60), start_text="demand_data.xlsx")#WIDTH / 2,  HEIGHT / 2, 400, font)
xlsx_path = pygame.sprite.Group(xlsx_input_box)

stress_mod_for_turn_box = TextInputBox(10,  HEIGHT / 2+300, 400, pygame.font.SysFont(None, 60), start_text="0.05; 0.05; 0.05; 0.05")#WIDTH / 2,  HEIGHT / 2, 400, font)
stress_mod_for_turn = pygame.sprite.Group(stress_mod_for_turn_box)


target_inventory_box = TextInputBox(10,  HEIGHT / 2-250, 400, pygame.font.SysFont(None, 60), start_text="20; 20; 20; 20")#WIDTH / 2,  HEIGHT / 2, 400, font)
target_inventory = pygame.sprite.Group(target_inventory_box)
   
    


running = True
while running:
    # Очистка окна
    menu_window.fill(BLUE)
    
    
    clock.tick(60)
    # Обработка событий
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий клавиш
        elif event.type == pygame.KEYDOWN and not text_input_box.active and not xlsx_input_box.active and not stress_mod_for_turn_box.active and not target_inventory_box.active:
            # Ввод имени игрока
            if event.key == pygame.K_1:
                game = Game()
                game.main(text_input_box.text.split('; '), xlsx_input_box.text, stress_mod_for_turn_box.text.split('; '), target_inventory_box.text.split('; '), use_stress, regime_native)#players_list, file_path,
            elif event.key == pygame.K_2:
               regime_native = not regime_native
            
            
            elif event.key == pygame.K_3:
                use_stress = not use_stress
                

    # Отрисовка текста
    
    text = font.render("Главное меню", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 350))
    menu_window.blit(text, text_rect)

    text = font.render("Минимум на складе", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 300))
    menu_window.blit(text, text_rect)


    
    text = font.render("1) Старт игры", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 200))
    menu_window.blit(text, text_rect)
    
    
    
    
    
    # Имя игрока
    text = font.render("Имена игроков: ", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 -150))
    menu_window.blit(text, text_rect)
    
    
    regime_text = "Продвинутая" if regime_native else "Наивная"
    text = font.render("2) Режим дозаказа: " + regime_text, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    menu_window.blit(text, text_rect)
    
    
    stres_text = "Включен" if use_stress else "Выключен"
    text = font.render("3) Стресс: " + stres_text, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
    menu_window.blit(text, text_rect)

   
    
    text = font.render("4) xlsx с данными: ", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
    menu_window.blit(text, text_rect)

   
    text = font.render("5) Стресс за ход: ", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 250))
    menu_window.blit(text, text_rect)

    target_inventory.update(event_list)
    target_inventory.draw(menu_window)
    stress_mod_for_turn.update(event_list)
    stress_mod_for_turn.draw(menu_window)
    # Обновление экрана
    xlsx_path.update(event_list)
    xlsx_path.draw(menu_window)
    
    players_list.update(event_list)
   
    players_list.draw(menu_window)
    
    pygame.display.flip()

pygame.quit()
