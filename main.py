import os
import pygame
import sys
import random
from src.player import Player
from src.alien import Alien
from src.bullet import Bullet
from src.alien_bullet import AlienBullet
from src.highscores import add_highscore, read_highscores
from src.explosion import Explosion

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

MAIN_MENU = 'main_menu'
PAUSED = 'paused'
PLAYING = 'playing'
GAME_OVER = 'game_over'
LEVEL_COMPLETE = 'level_complete'

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Remastered")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/background_music.ogg")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load sound effects
player_shoot_sound = pygame.mixer.Sound("assets/sounds/player_shoot.wav")
alien_shoot_sound = pygame.mixer.Sound("assets/sounds/alien_shoot.wav")
alien_hit_sound = pygame.mixer.Sound("assets/sounds/alien_hit.wav")
player_hit_sound = pygame.mixer.Sound("assets/sounds/player_hit.wav")
game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")

def load_scaled_background(image_path, width, height):
    img = pygame.image.load(image_path)
    img_width, img_height = img.get_size()

    scale = max(width / img_width, height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    img = pygame.transform.scale(img, (new_width, new_height))

    return img

background_images = [
    load_scaled_background(os.path.join("assets", "images", "background1.jpg"), WIDTH, HEIGHT),
    load_scaled_background(os.path.join("assets", "images", "background2.jpg"), WIDTH, HEIGHT),
    load_scaled_background(os.path.join("assets", "images", "background3.jpg"), WIDTH, HEIGHT),
    load_scaled_background(os.path.join("assets", "images", "background4.jpg"), WIDTH, HEIGHT),
    load_scaled_background(os.path.join("assets", "images", "background5.jpg"), WIDTH, HEIGHT)
]

def create_random_alien_grid(aliens, screen, difficulty):
    alien_image_paths = [
        "assets/images/alien1.png",
        "assets/images/alien2.png",
        "assets/images/alien3.png",
    ]
    alien_rows = random.randint(3, 5)
    alien_columns = random.randint(8, 12)

    for row in range(alien_rows):
        for column in range(alien_columns):
            if random.random() < 0.8:
                x = 50 + column * 60
                y = 50 + row * 60

                # Determine the alien type based on the level
                alien_type = min(level, len(alien_image_paths)) - 1
                alien_image_path = alien_image_paths[alien_type]

                alien = Alien(x, y, screen, alien_image_path, speed_multiplier=difficulty)
                aliens.add(alien)
                all_sprites.add(alien)

def draw_text(surface, text, size, x, y, color=(255, 255, 255), align='center'):
    font = pygame.font.Font("assets/fonts/valorax.otf", size)  # Update the font path accordingly
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == 'right':
        text_rect.topright = (x, y)
    else:
        text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_title(surface, text, size, x, y, color=(255, 255, 255)):
    font_name="assets/fonts/valorax.otf"
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def reset_game():
    global all_sprites, aliens, player_bullets, alien_bullets, player, level, score, game_over

    all_sprites.empty()
    aliens.empty()
    player_bullets.empty()
    alien_bullets.empty()

    player = Player(WIDTH // 2 - 32, HEIGHT - 100, screen, 3)
    all_sprites.add(player)

    create_random_alien_grid(aliens, screen, level * 0.2)

    level = 1
    score = 0
    game_over = False

def next_level():
    global all_sprites, aliens, player_bullets, alien_bullets, player, level, background_image_index

    pygame.mixer.music.set_volume(0.4)
    all_sprites.empty()
    aliens.empty()
    player_bullets.empty()
    alien_bullets.empty()

    lives = player.lives
    if lives == 3:
        lives += 1
    elif level % 3 == 0:
        lives = 3
    player = Player(WIDTH // 2 - 32, HEIGHT - 100, screen, lives)
    all_sprites.add(player)

    create_random_alien_grid(aliens, screen, level * 0.2)

    level += 1
    background_image_index = (background_image_index + 1) % len(background_images)

def show_menu():
    global game_state
    
    pygame.mixer.music.set_volume(0.4)
    menu = True
    selected_option = 0
    options = ["Start Game", "Leaderboard", "Quit"]
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        menu = False
                        game_state = PLAYING
                    elif selected_option == 1:
                        show_leaderboard()
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()

        bg_img = load_scaled_background(os.path.join("assets", "images", "space_background.jpg"), WIDTH, HEIGHT)
        bg_x = (WIDTH - bg_img.get_width()) // 2
        bg_y = (HEIGHT - bg_img.get_height()) // 2
        screen.blit(bg_img, (bg_x, bg_y))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(178)  # 40% opacity (255 * 0.4 = 102)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        draw_title(screen, "Space Invaders", 60, WIDTH // 2, HEIGHT // 2 - 200, color=(105, 99, 255))
        draw_title(screen, "Remastered", 40, WIDTH // 2, HEIGHT // 2 - 140, color=(99, 213, 255))

        for idx, option in enumerate(options):
            color = (255, 255, 255) if idx == selected_option else (100, 100, 100)
            draw_text(screen, option, 32, WIDTH // 2, HEIGHT // 2 - 40 + idx * 60, color=color)

        pygame.display.flip()
        clock.tick(FPS)

def show_leaderboard():
    leaderboard = True
    while leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leaderboard = False

        screen.fill((0, 0, 0))
        draw_text(screen, "Leaderboard", 60, WIDTH // 2, HEIGHT // 2 - 200, color=(99, 213, 255))

        with open("highscores.txt", "r") as file:
            highscores = [int(line.strip()) for line in file.readlines()]

        for idx, score in enumerate(highscores):
            draw_text(screen, f"{idx + 1}. {score}", 32, WIDTH // 2, HEIGHT // 2 - 100 + idx * 40)

        draw_text(screen, "Press ESC to go back", 14, WIDTH // 2, HEIGHT - 60)

        pygame.display.flip()
        clock.tick(FPS)

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()

# Create player instance
player = Player(WIDTH // 2 - 32, HEIGHT - 100, screen, 3)
all_sprites.add(player)

alien_shoot_cooldown = 0
background_image_index = 0
score = 0
level = 1

# Create a random grid of aliens
create_random_alien_grid(aliens, screen, level * 0.2)

game_over = False
game_state = MAIN_MENU
level_complete = False
paused = False
player_rank = None

black_overlay = pygame.Surface((WIDTH, HEIGHT))
black_overlay.set_alpha(102)  # 40% opacity (255 * 0.4 = 102)
black_overlay.fill((0, 0, 0))

def handle_gameplay():
    global game_over, level_complete, game_state, alien_shoot_cooldown, score, player_rank

    pygame.mixer.music.set_volume(0.4)
    set_space_background()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.reset_tilt()

    if player.lives <= 0 and not game_over:
        game_over = True
        game_state = GAME_OVER
        highscores = add_highscore(score)
        if score in highscores:
            player_rank = highscores.index(score) + 1

    if len(aliens) == 0:
        game_state = LEVEL_COMPLETE
    else:
        # Player bullet and alien collision detection
        collisions = pygame.sprite.groupcollide(aliens, player_bullets, True, True)
        for hit in collisions:
            alien_hit_sound.play()
            score += 100
            explosion = Explosion(hit.rect.centerx, hit.rect.centery, screen)
            all_sprites.add(explosion)
        
        # Check for collisions between player and alien bullets
        player_hit = pygame.sprite.spritecollide(player, alien_bullets, True)
        if player_hit:
            player_hit_sound.play()
            player.lives -= 1

        # Alien shooting
        if alien_shoot_cooldown <= 0 and len(aliens.sprites()) > 0:
            alien_shoot_sound.play()
            shooting_alien = random.choice(aliens.sprites())
            alien_bullet = AlienBullet(shooting_alien.rect.centerx, shooting_alien.rect.bottom, screen)
            all_sprites.add(alien_bullet)
            alien_bullets.add(alien_bullet)
            alien_shoot_cooldown = random.randint(max(10, 60 - level * 5), max(20, 80 - level * 5))
        else:
            alien_shoot_cooldown -= 1

        all_sprites.update()
        all_sprites.draw(screen)

        # Display score and lives
        draw_text(screen, "Score: " + str(score), 16, WIDTH - 10, 10, color=(0, 255, 0), align='right')
        draw_text(screen, "Lives: " + str(player.lives), 16, WIDTH - 10, 30, color=(0, 255, 0), align='right')
        draw_text(screen, "Level: " + str(level), 16, 50, 10, color=(255, 255, 255), align='left')

    pygame.display.flip()
    clock.tick(FPS)

def handle_game_over():
    global player_rank

    pygame.mixer.music.set_volume(0.2)
    set_space_background()

    highscores = add_highscore(score)
    if score in highscores:
        player_rank = highscores.index(score) + 1

    highscores = read_highscores()
    number_of_highscores = len(highscores)
    draw_text(screen, "Game Over", 60, WIDTH // 2, HEIGHT // 2 - 140, color=(255, 0, 0))
    draw_text(screen, f"Score: {score}", 40, WIDTH // 2, HEIGHT // 2 - 60, color=(255, 255, 255))
    if number_of_highscores > 0:
        draw_text(screen, "High Scores", 24, WIDTH // 2, HEIGHT // 2, color=(200, 200, 200))
        for i, hs in enumerate(highscores):
            y = HEIGHT // 2 + 40 + i * 20
            text = f"{i+1}. {hs}"
            color = (200, 200, 200) if hs != score else (255, 255, 0)
            draw_text(screen, text, 16, WIDTH // 2, y, color=color)
        if score in highscores:
            rank = highscores.index(score) + 1
            draw_text(screen, f"Your rank: {rank}", 20, WIDTH // 2, HEIGHT // 2 + 70 + (number_of_highscores - 1) * 20, color=(255, 255, 255))
    draw_text(screen, "Press SPACE to start new game", 14, WIDTH // 2, HEIGHT // 2 + 140 + (number_of_highscores - 1) * 20, color=(180, 180, 180))
    draw_text(screen, "Press ESC to go to main menu", 14, WIDTH // 2, HEIGHT // 2 + 160 + (number_of_highscores - 1) * 20, color=(180, 180, 180))

    pygame.display.flip()
    clock.tick(FPS)

def handle_paused():
    pygame.mixer.music.set_volume(0.2)
    set_space_background()
    draw_text(screen, "Paused", 60, WIDTH // 2, HEIGHT // 2 - 80, color=(255, 196, 0))
    draw_text(screen, "Press SPACE to resume", 14, WIDTH // 2, HEIGHT // 2 + 30, color=(180, 180, 180))
    draw_text(screen, "Press ESC to go to main menu", 14, WIDTH // 2, HEIGHT // 2 + 60, color=(180, 180, 180))

    pygame.display.flip()
    clock.tick(FPS)

def handle_level_complete():
    pygame.mixer.music.set_volume(0.2)

    draw_text(screen, "Level " + str(level) + " Complete", 45, WIDTH // 2, HEIGHT // 2 - 80, color=(0, 255, 0))
    draw_text(screen, f"Score: {score}", 32, WIDTH // 2, HEIGHT // 2, color=(255, 255, 255))
    draw_text(screen, "Press SPACE to continue", 14, WIDTH // 2, HEIGHT // 2 + 80, color=(180, 180, 180))

    pygame.display.flip()
    clock.tick(FPS)

def set_space_background():
    bg_img = background_images[background_image_index]
    bg_x = (WIDTH - bg_img.get_width()) // 2
    bg_y = (HEIGHT - bg_img.get_height()) // 2
    screen.blit(bg_img, (bg_x, bg_y))
    screen.blit(black_overlay, (0, 0))

# Main game loop
while True:
    # Main Menu
    if game_state == MAIN_MENU:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
                elif event.key == pygame.K_l:
                    show_leaderboard()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Playing
    elif game_state == PLAYING:
        handle_gameplay()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSED
                    break
                if event.key == pygame.K_SPACE:
                    player_shoot_sound.play()
                    bullet = Bullet(player.rect.centerx, player.rect.top, screen)
                    all_sprites.add(bullet)
                    player_bullets.add(bullet)

    # Paused
    elif game_state == PAUSED:
        handle_paused()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    game_state = MAIN_MENU
                    reset_game()

    # Game Over
    elif game_state == GAME_OVER:
        handle_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    game_state = MAIN_MENU
                    reset_game()
                elif event.key == pygame.K_m:
                    game_state = MAIN_MENU
                    reset_game()

    # Game Over
    elif game_state == LEVEL_COMPLETE:
        handle_level_complete()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    next_level()
                    game_state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    game_state = MAIN_MENU
                    reset_game()
                elif event.key == pygame.K_m:
                    game_state = MAIN_MENU
                    reset_game()
