# import pygame

# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y, screen):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.screen = screen
#         self.image = pygame.Surface((4, 10))  # Adjust the size as needed
#         self.image.fill((255, 255, 255))  # Set the bullet color
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)

#     def update(self):
#         self.y -= 10  # Adjust the speed value as desired
#         self.rect.y = self.y
#         if self.y < 0:
#             self.kill()

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self):
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)
        if self.rect.bottom < 0:
            self.kill()

