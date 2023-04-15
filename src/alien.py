import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, image_path, speed_multiplier=1.0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (40, 40))  # Scale the image to the desired size (e.g., 40x40 pixels)
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
