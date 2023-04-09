import pygame
import sys
import random
from src.player import Player
from src.alien import Alien
from src.bullet import Bullet
from src.alien_bullet import AlienBullet

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Remastered")
clock = pygame.time.Clock()

def create_random_alien_grid(aliens, screen):
    alien_image_path = "assets/images/alien.png"
    alien_rows = random.randint(3, 5)
    alien_columns = random.randint(8, 12)

    for row in range(alien_rows):
        for column in range(alien_columns):
            if random.random() < 0.8:
                x = 50 + column * 60
                y = 50 + row * 60
                alien = Alien(x, y, screen, alien_image_path)
                aliens.add(alien)
                all_sprites.add(alien)

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()

# Create player instance
player = Player(WIDTH // 2 - 32, HEIGHT - 100, screen)
all_sprites.add(player)

# Create a random grid of aliens
create_random_alien_grid(aliens, screen)

alien_shoot_cooldown = 0

# Main game loop
while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top, screen)
                all_sprites.add(bullet)
                player_bullets.add(bullet)

    screen.fill((0, 0, 0))
    
    # Player bullet and alien collision detection
    collisions = pygame.sprite.groupcollide(aliens, player_bullets, True, True)
    
    # Check for collisions between player and alien bullets
    player_hit = pygame.sprite.spritecollide(player, alien_bullets, True)
    if player_hit:
        # Handle player hit, e.g., reduce lives, end the game, etc.
        pass
    
    # Alien shooting
    if alien_shoot_cooldown <= 0:
        shooting_alien = random.choice(aliens.sprites())
        alien_bullet = AlienBullet(shooting_alien.rect.centerx, shooting_alien.rect.bottom, screen)
        all_sprites.add(alien_bullet)
        alien_bullets.add(alien_bullet)
        alien_shoot_cooldown = random.randint(40, 60)
    else:
        alien_shoot_cooldown -= 1

    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
