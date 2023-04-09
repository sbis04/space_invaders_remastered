import pygame

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.screen = screen

        self.rect.centerx = x
        self.rect.top = y

        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > self.screen.get_rect().bottom:
            self.kill()
