import pygame
from src.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        image = pygame.image.load('assets/images/player_ship.png')
        self.image = pygame.transform.scale(image, (64, 64))  # Scale the image to the desired size (e.g., 64x64 pixels)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move_left(self):
        self.x -= 5  # Adjust the speed value as desired
        if self.x < 0:
            self.x = 0
        self.rect.x = self.x

    def move_right(self):
        self.x += 5  # Adjust the speed value as desired
        if self.x > self.screen.get_width() - self.rect.width:
            self.x = self.screen.get_width() - self.rect.width
        self.rect.x = self.x

    def shoot(self, bullets, all_sprites):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.screen)
        bullets.add(bullet)
        all_sprites.add(bullet)

    # def shoot(self, all_sprites):
    #     bullet = Bullet(self.x + self.rect.width // 2 - 2, self.y, self.screen)
    #     self.screen.blit(bullet.image, bullet.rect)
    #     all_sprites.add(bullet)
