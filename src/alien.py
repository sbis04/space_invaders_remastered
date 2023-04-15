import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, image_path, speed_multiplier=1.0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        # Load the image and set its rect attribute
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Scale the image while maintaining its aspect ratio
        desired_width = 50  # Set the desired width for the alien images
        aspect_ratio = float(self.image.get_height()) / float(self.image.get_width())
        new_size = (desired_width, int(desired_width * aspect_ratio))
        self.image = pygame.transform.scale(self.image, new_size)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set the alien's speed
        self.speedx = random.choice([-1, 1]) * (2 + speed_multiplier)
        self.speedy = random.choice([-1, 1]) * (1 + speed_multiplier)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.speed *= speed_multiplier
        self.direction = 1

    def update(self):
        self.x += self.speed * self.direction
        self.rect.topleft = (self.x, self.y)

        # Check if the alien has reached the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.left <= screen_rect.left or self.rect.right >= screen_rect.right:
            self.direction *= -1
            self.y += 40  # Move down by 40 pixels
            self.x += self.speed * self.direction
            self.rect.topleft = (self.x, self.y)
