import pygame
from src.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, lives):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        image = pygame.image.load('assets/images/player_ship.png')
        sizedImage = pygame.transform.scale(image, (64, 64))
        self.original_image = sizedImage.convert_alpha()
        self.image = self.original_image.copy()
        # self.image = pygame.transform.scale(image, (64, 64))  # Scale the image to the desired size (e.g., 64x64 pixels)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.lives = lives
        self.speed = 5

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def move_left(self):
        self.x -= self.speed # Adjust the speed value as desired
        if self.x < 0:
            self.x = 0
        self.set_tilt(5)
        self.rect.x = self.x

    def move_right(self):
        self.x += self.speed  # Adjust the speed value as desired
        if self.x > self.screen.get_width() - self.rect.width:
            self.x = self.screen.get_width() - self.rect.width
        self.rect.x = self.x
        self.set_tilt(-5)

    def shoot(self, bullets, all_sprites):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.screen)
        bullets.add(bullet)
        all_sprites.add(bullet)

    def set_tilt(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_tilt(self):
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.rect.center)
