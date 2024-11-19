from graphics import *  # Zelle's Graphics for the start screen
import pygame           # Pygame for the main game
import random

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Load images
sky_background = pygame.image.load("sky_background.png")
superhero_image = pygame.image.load("superhero.png")
building_image = pygame.image.load("building.png")
shield_image = pygame.image.load("shield.png")
score_boost_image = pygame.image.load("score_boost.png")

# Scale images
sky_background = pygame.transform.scale(sky_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
superhero_image = pygame.transform.scale(superhero_image, (50, 80))
building_image = pygame.transform.scale(building_image, (100, 300))
shield_image = pygame.transform.scale(shield_image, (30, 30))
score_boost_image = pygame.transform.scale(score_boost_image, (30, 30))

# Audio
pygame.mixer.music.load("background_music.mp3")
power_up_sound = pygame.mixer.Sound("power_up_sound.wav")

# Game variables
superhero_rect = superhero_image.get_rect(center=(100, SCREEN_HEIGHT // 2))
score = 0
health = 5
building_speed = 5
power_up_speed = 5
power_up_active = False
power_up_start_time = 0
power_up_duration = 5000
font = pygame.font.Font(None, 36)  # Pygame font for text rendering

# Pygame obstacles and power-ups
buildings = []
power_ups = []

# Global Pygame screen variable
screen = None

# Function to display the start screen using Zelle's Graphics
def start_screen():
    win = GraphWin("Sky Trek - Start Screen", SCREEN_WIDTH, SCREEN_HEIGHT)
    win.setBackground("black")
    
    start_text = Text(Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), "Welcome to Sky Trek!")
    start_text.setSize(24)
    start_text.setTextColor("white")
    start_text.draw(win)
    
    start_button = Rectangle(Point(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2), Point(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 40))
    start_button.setFill("yellow")
    start_button.draw(win)
    
    start_button_text = Text(start_button.getCenter(), "Start Game")
    start_button_text.setSize(12)
    start_button_text.setTextColor("black")
    start_button_text.draw(win)
    
    while True:
        click_point = win.getMouse()
        if (start_button.getP1().getX() <= click_point.getX() <= start_button.getP2().getX() and
                start_button.getP1().getY() <= click_point.getY() <= start_button.getP2().getY()):
            win.close()  # Close the Zelle's Graphics window
            break

# Function to display text on the Pygame screen
def display_text(text, x, y, color=WHITE):
    """Renders text on the screen."""
    global screen
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Function to spawn buildings
def spawn_building():
    building_x = SCREEN_WIDTH
    building_y = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 100)
    building_rect = building_image.get_rect(topleft=(building_x, building_y))
    buildings.append(building_rect)

# Function to spawn power-ups
def spawn_power_up():
    power_up_x = SCREEN_WIDTH
    power_up_y = random.randint(50, SCREEN_HEIGHT - 50)
    power_up_type = random.choice(["shield", "score_boost"])
    power_up_image = shield_image if power_up_type == "shield" else score_boost_image
    power_up_rect = power_up_image.get_rect(topleft=(power_up_x, power_up_y))
    power_ups.append({"rect": power_up_rect, "type": power_up_type, "image": power_up_image})

# Function to reset the game
def reset_game():
    global buildings, power_ups, score, health, power_up_active
    buildings = []
    power_ups = []
    score = 0
    health = 5
    power_up_active = False
    superhero_rect.y = SCREEN_HEIGHT // 2

# Main game loop using Pygame
def game_loop():
    """Main game loop to handle gameplay."""
    global score, health, power_up_active, power_up_start_time, screen
    running = True
    game_over = False
    clock = pygame.time.Clock()
    bg_x = 0

    # Start Pygame screen
    pygame.display.set_caption("Sky Trek - Main Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Play background music
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and superhero_rect.top > 0:
            superhero_rect.y -= 5
        if keys[pygame.K_DOWN] and superhero_rect.bottom < SCREEN_HEIGHT:
            superhero_rect.y += 5

        # Draw background
        screen.blit(sky_background, (bg_x, 0))
        screen.blit(sky_background, (bg_x + SCREEN_WIDTH, 0))
        bg_x -= 2
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

        # Spawn buildings and power-ups
        if random.randint(1, 60) == 1:
            spawn_building()
        if random.randint(1, 300) == 1:
            spawn_power_up()

        # Update buildings
        for building in buildings[:]:
            building.x -= building_speed
            if building.right < 0:
                buildings.remove(building)
                score += 1
            elif building.colliderect(superhero_rect):
                health -= 1
                buildings.remove(building)
                if health <= 0:
                    game_over = True
            screen.blit(building_image, building)

        # Update power-ups
        for power_up in power_ups[:]:
            power_up["rect"].x -= power_up_speed
            if power_up["rect"].colliderect(superhero_rect):
                power_up_sound.play()
                if power_up["type"] == "shield":
                    power_up_active = True
                    power_up_start_time = pygame.time.get_ticks()
                elif power_up["type"] == "score_boost":
                    score += 10
                power_ups.remove(power_up)
            elif power_up["rect"].right < 0:
                power_ups.remove(power_up)
            else:
                screen.blit(power_up["image"], power_up["rect"])

        # Handle power-up expiration
        if power_up_active:
            if pygame.time.get_ticks() - power_up_start_time > power_up_duration:
                power_up_active = False

        # Draw superhero
        screen.blit(superhero_image, superhero_rect)

        # Display score and health
        display_text(f"Score: {score}", 10, 10)
        display_text(f"Health: {health}", 10, 40)

        # Handle game over
        if game_over:
            screen.fill(BLACK)
            display_text(f"Game Over! Final Score: {score}", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
            display_text("Press 'R' to Restart or 'Q' to Quit", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20)
            pygame.display.flip()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Show the start screen using Zelle's Graphics
start_screen()

# Run the game loop in Pygame
game_loop()
