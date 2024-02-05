import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800*2, 600*2
PLAYER_SIZE = 100
BOT_SIZE = 100
BULLET_SIZE = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Tanks Game")

# Load background image
background_image = pygame.image.load('backgroundTank.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load player tank image
player_tank_image = pygame.image.load('tank.png')
player_tank_image = pygame.transform.scale(player_tank_image, (PLAYER_SIZE, PLAYER_SIZE))

# Load bullet image
bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (BULLET_SIZE, BULLET_SIZE))

# Load bot tank image
bot_tank_image = pygame.image.load('tankEnemy.png')
bot_tank_image = pygame.transform.scale(bot_tank_image, (BOT_SIZE, BOT_SIZE))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player tank
player_x = WIDTH // 4
player_y = HEIGHT // 2
player_speed = 5
player_health = 3
player_score = 0

# Bot tank
bot_x = 3 * WIDTH // 4
bot_y = HEIGHT // 2
bot_speed = 3
bot_health = 3
bot_shoot_delay = 60  # Delay between bot shots (in frames)
bot_shoot_timer = 0
bot_response_timer = 0
bot_response_duration = 10  # Duration of the bot response animation (in frames)
bot_bullet_list = []

# Second bot tank (added)
second_bot_x = WIDTH // 2
second_bot_y = HEIGHT // 4
second_bot_speed = 3
second_bot_health = 3
second_bot_shoot_delay = 60
second_bot_shoot_timer = 0
second_bot_bullet_list = []

# Bullets
player_bullet_list = []
bot_bullet_list = []
second_bot_bullet_list = []

# Particle effect parameters
particle_list = []

# Pause flag
paused = False

# Lighting surface
light_mask = pygame.Surface((WIDTH, HEIGHT))
light_mask.set_alpha(100)

# Particle function for player
def create_particles(x, y, color):
    num_particles = 10
    for _ in range(num_particles):
        particle_list.append([x, y, random.randint(2, 5), random.uniform(0, 2 * math.pi), color])

# Particle function for bot
def create_bot_particles(x, y, color):
    num_particles = 10
    for _ in range(num_particles):
        particle_list.append([x, y, random.randint(2, 5), random.uniform(0, 2 * math.pi), color])

# Functions
def draw_particles(particle_list):
    for particle in particle_list:
        pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), 2)

# Functions
def draw_tank(x, y, image=None, color=None):
    if image:
        screen.blit(image, (x, y))
    elif color:
        pygame.draw.rect(screen, color, [x, y, PLAYER_SIZE, PLAYER_SIZE])

def draw_bullet(bullet_list, image):
    for bullet in bullet_list:
        screen.blit(image, (bullet[0], bullet[1]))

def collision(obj1, obj2):
    if isinstance(obj1, list):
        rect1 = pygame.Rect(obj1[0], obj1[1], BULLET_SIZE, BULLET_SIZE)
    else:
        rect1 = pygame.Rect(obj1)
    rect2 = pygame.Rect(obj2)
    return rect1.colliderect(rect2)

def restart_game():
    global player_health, player_score, player_x, player_y, bot_health, bot_x, bot_y, bot_bullet_list, second_bot_health, second_bot_x, second_bot_y, second_bot_bullet_list
    player_health = 3
    player_score = 0
    player_x = WIDTH // 4
    player_y = HEIGHT // 2
    bot_health = 3
    bot_x = 3 * WIDTH // 4
    bot_y = HEIGHT // 2
    bot_bullet_list = []  # Reset bot's bullet list

    # Reset second bot (added)
    second_bot_health = 3
    second_bot_x = WIDTH // 2
    second_bot_y = HEIGHT // 4
    second_bot_bullet_list = []

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire bullet
                player_bullet_list.append([player_x + PLAYER_SIZE, player_y + PLAYER_SIZE // 2])
                create_particles(player_x + PLAYER_SIZE, player_y + PLAYER_SIZE // 2, (255, 165, 0))  # Create orange particles when bullet is launched
            elif event.key == pygame.K_p:
                # Toggle pause
                paused = not paused
            elif event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r and player_health == 0:
                # Restart the game
                restart_game()

    if not paused:
        if player_health > 0:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_SIZE:
                player_y += player_speed

            # Bot movement towards the player
            angle = math.atan2(player_y - bot_y, player_x - bot_x)
            bot_x += bot_speed * math.cos(angle)
            bot_y += bot_speed * math.sin(angle)

            # Second bot movement towards the player (added)
            angle_second_bot = math.atan2(player_y - second_bot_y, player_x - second_bot_x)
            second_bot_x += second_bot_speed * math.cos(angle_second_bot)
            second_bot_y += second_bot_speed * math.sin(angle_second_bot)

            # Ensure the bots stay off-screen initially
            if bot_x < 0:
                bot_x = WIDTH
                bot_y = random.randint(0, HEIGHT - BOT_SIZE)
            if second_bot_x < 0:  # Added
                second_bot_x = WIDTH
                second_bot_y = random.randint(0, HEIGHT - BOT_SIZE)

            # Bullet movement and collision detection for player
            for bullet in player_bullet_list:
                bullet[0] += 5
                if bullet[0] > WIDTH:
                    player_bullet_list.remove(bullet)
                    create_particles(bullet[0], bullet[1], (255, 165, 0))  # Create orange particles when bullet is launched
                elif collision(bullet, [bot_x, bot_y, BOT_SIZE, BOT_SIZE]):
                    player_bullet_list.remove(bullet)
                    bot_health -= 1
                    bot_response_timer = bot_response_duration  # Trigger bot response animation
                    if bot_health == 0:
                        bot_x = WIDTH  # Start off-screen
                        bot_y = random.randint(0, HEIGHT - BOT_SIZE)
                        bot_health = 3
                        player_score += 1

                # Collision detection for second bot (added)
                elif collision(bullet, [second_bot_x, second_bot_y, BOT_SIZE, BOT_SIZE]):
                    player_bullet_list.remove(bullet)
                    second_bot_health -= 1
                    bot_response_timer = bot_response_duration  # Trigger bot response animation
                    if second_bot_health == 0:
                        second_bot_x = WIDTH  # Start off-screen
                        second_bot_y = random.randint(0, HEIGHT - BOT_SIZE)
                        second_bot_health = 3
                        player_score += 1

            # Bullet movement and collision detection for bots
            for bullet in bot_bullet_list:
                bullet[0] -= 5
                if bullet[0] < 0:
                    bot_bullet_list.remove(bullet)
                    create_bot_particles(bullet[0], bullet[1], (255, 165, 0))  # Create orange particles when bot's bullet is launched
                elif collision(bullet, [player_x, player_y, PLAYER_SIZE, PLAYER_SIZE]):
                    bot_bullet_list.remove(bullet)
                    player_health -= 1
                    if player_health == 0:
                        print("Game Over - Press 'r' to restart!")

            # Bullet movement and collision detection for second bot (added)
            for bullet in second_bot_bullet_list:
                bullet[0] -= 5
                if bullet[0] < 0:
                    second_bot_bullet_list.remove(bullet)
                    create_bot_particles(bullet[0], bullet[1], (255, 165, 0))  # Create orange particles when bot's bullet is launched
                elif collision(bullet, [player_x, player_y, PLAYER_SIZE, PLAYER_SIZE]):
                    second_bot_bullet_list.remove(bullet)
                    player_health -= 1
                    if player_health == 0:
                        print("Game Over - Press 'r' to restart!")

            # Particle movement
            for particle in particle_list:
                particle[0] += particle[2] * math.cos(particle[3])
                particle[1] += particle[2] * math.sin(particle[3])
                particle[2] -= 0.1  # Particle fade-out effect
                if particle[2] <= 0:
                    particle_list.remove(particle)

            # Add logic for bots to shoot bullets
            bot_shoot_timer -= 1
            if bot_shoot_timer <= 0:
                bot_bullet_list.append([bot_x, bot_y + BOT_SIZE // 2])
                create_bot_particles(bot_x, bot_y + BOT_SIZE // 2, (255, 165, 0))  # Create orange particles when bot's bullet is launched
                bot_shoot_timer = bot_shoot_delay

            # Second bot shooting logic (added)
            second_bot_shoot_timer -= 1
            if second_bot_shoot_timer <= 0:
                second_bot_bullet_list.append([second_bot_x, second_bot_y + BOT_SIZE // 2])
                create_bot_particles(second_bot_x, second_bot_y + BOT_SIZE // 2, (255, 165, 0))  # Create orange particles when bot's bullet is launched
                second_bot_shoot_timer = second_bot_shoot_delay

        else:
            # Player is out of health, prompt for restart
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart_game()

    # Draw everything
    screen.blit(background_image, (0, 0))  # Draw the background

    # Draw lighting effect
    screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    draw_tank(player_x, player_y, image=player_tank_image)
    draw_tank(bot_x, bot_y, image=bot_tank_image)
    draw_tank(second_bot_x, second_bot_y, image=bot_tank_image)  # Draw second bot (added)
    draw_bullet(player_bullet_list, bullet_image)
    draw_bullet(bot_bullet_list, bullet_image)
    draw_bullet(second_bot_bullet_list, bullet_image)  # Draw second bot bullets (added)
    draw_particles(particle_list)

    # Display health and score
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    score_text = font.render(f"Score: {player_score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    # Display pause message
    if paused:
        pause_text = font.render("Game Paused", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))

    # Display restart prompt
    if player_health == 0:
        restart_prompt = font.render("Press 'r' to restart", True, WHITE)
        screen.blit(restart_prompt, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
