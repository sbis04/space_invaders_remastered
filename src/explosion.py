import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen
        self.images = []
        self.index = 0
        self.load_images()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.frame_counter = 0

    def load_images(self):
        for i in range(1, 12):  # 11 frames
            image_path = f"assets/images/explosion_{str(i).zfill(2)}.png"
            self.images.append(pygame.image.load(image_path).convert_alpha())

    def update(self):
        self.frame_counter += 1

        if self.frame_counter % 4 == 0:  # Control the animation speed
            self.index += 1

        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]

