import pygame
import sys
from src.player import Player
from src.alien import Alien
from src.bullet import Bullet

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Set the title
pygame.display.set_caption("Space Invaders Remastered")

# Create the Player instance and add it to a sprite group
player = Player(WIDTH // 2 - 32, HEIGHT - 100, screen)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create a grid of aliens
alien_rows = 5
alien_columns = 10
alien_spacing_x = 70
alien_spacing_y = 60
aliens = pygame.sprite.Group()

for row in range(alien_rows):
    for column in range(alien_columns):
        x = 50 + column * alien_spacing_x
        y = 50 + row * alien_spacing_y
        image_path = 'assets/images/alien.png'
        alien = Alien(x, y, screen, image_path)
        aliens.add(alien)
        all_sprites.add(alien)

# Create a sprite group for bullets
bullets = pygame.sprite.Group()

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot(bullets, all_sprites)

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Update
    all_sprites.update()

    # Check for collisions between bullets and aliens
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)

    # Check if any aliens have reached the bottom of the screen
    for alien in aliens:
        if alien.rect.bottom >= screen.get_rect().bottom:
            # End the game or implement any other desired behavior
            pygame.quit()
            sys.exit()

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()
    clock.tick(FPS)
