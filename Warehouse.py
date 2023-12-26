import pygame


class Warehouse(pygame.sprite.Sprite):
    def __init__(self, title='', size=None, color=(255, 255, 0), x=0, y=0):
        super().__init__()
        self.number = 0
        self.title = title
        if size is not None:  # в целях тестирования
            self.color = color
            self.size = size
            self.x = x
            self.y = y
            
    def draw(self, screen, font, sc=False):
        # Рисование квадратика
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        #print(self.x, self.y, self.size)
        # Отображение номера на квадратике
        text = font.render(str(self.number), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x+self.size//2, self.y+self.size//2))
        screen.blit(text, text_rect)
        
        # Отображение заголовка на квадратике
        text = font.render(str(self.title), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x+self.size//2, int(self.y-self.size//2)))
        screen.blit(text, text_rect)
        if sc:
            # Отображение заголовка на квадратике
            text = font.render('долг: '+str(sc), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x+self.size//2, int(self.y+self.size*1.5)))
            screen.blit(text, text_rect)
        

        '''
        # Передвижение квадратика
        if x < point_b[0]:
            x += 1
        elif x > point_b[0]:
            x -= 1
        if y < point_b[1]:
            y += 1
        elif y > point_b[1]:
            y -= 10
        #'''
        
        
        '''
        if size is not None:  # в целях тестирования
            self.image = pygame.Surface((size, size))
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft=(x, y))

    shape = [
        'xxxxxxxxxxxxxxxx',
        'xxxxxxxxxxxxxxxx',
        'xxxxxxxxxxxxxxxx',
        'xxxxxxxxxxxxxxxx',
        'xxxxxxxxxxxxxxxx',
    ]
        #'''

