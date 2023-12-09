import pygame


class Warehouse(pygame.sprite.Sprite):
    def __init__(self, size=None, color=0, x=0, y=0):
        super().__init__()
        self.number = 0
        if size is not None:#в целях тестирования
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
