import pygame
from pygame.draw import circle
import Button

pygame.init()
pygame.font.init()

# Create a font object
font = pygame.font.Font("freesansbold.ttf", 30)

WIDTH = 600
LENGTH = 600
screen = pygame.display.set_mode((WIDTH, LENGTH))    # determines screen size
pygame.display.set_caption("My first game")     # Window title

img = pygame.image.load("flooring.png")
background = pygame.transform.scale(img, screen.get_size())

# Predefined colors
LIGHT_GREEN = (181, 238, 174)
LIGHT_BLUE = (100, 150, 200)
PINK = (227, 165, 192)
RED = (180, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = pygame.time.Clock()
framerate = 60

# Global coordinate Variables
x = 200
y = 200


# Load in our sprites here
player_left = pygame.image.load("walk_left.png")
player_left = pygame.transform.scale_by(player_left, 2)

player_right = pygame.image.load("walk_right.png")
player_right = pygame.transform.scale_by(player_right, 2)

player_up = pygame.image.load("walk_up.png")
player_up = pygame.transform.scale_by(player_up, 2)

player_down = pygame.image.load("walk_left.png")
player_down = pygame.transform.scale_by(player_down, 2)

# Default sprite
current_sprite = player_left
current_rect = current_sprite.get_rect()

circle_color = PINK

states = ["menu", "running", "end"]
current_state = "menu"

running = True
while running:

    FPS.tick(framerate)

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:   # Determine if the user hit quit
            running = False

    # Let's determine user input
    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_LEFT] and current_rect.x > 0:
        # print("The user pressed the left button")
        current_rect.x = current_rect.x - 10
        current_sprite = player_left

    if user_input[pygame.K_RIGHT] and current_rect.x + current_sprite.get_width() < WIDTH:
        # print("The user pressed the right button")
        current_rect.x = current_rect.x + 10
        current_sprite = player_right

    if user_input[pygame.K_DOWN] and current_rect.y + current_sprite.get_height() < LENGTH:
        # print("The user pressed the down button")
        current_rect.y = current_rect.y + 10
        current_sprite = player_down

    if user_input[pygame.K_UP] and current_rect.y > 0:
        # print("The user pressed the up button")
        current_rect.y = current_rect.y - 10
        current_sprite = player_up

    # Note: These should be moved to functions later!
    # screen.fill(LIGHT_BLUE)  # Fills the screen with a light blue background!
    screen.blit(background, (0, 0))

    # Let's make a rectangle
    my_rectangle = pygame.Rect(100, 200, 200, 100)
    pygame.draw.rect(screen, RED, my_rectangle)

    # Create the sprite
    screen.blit(current_sprite, (current_rect.x, current_rect.y))

    pos = pygame.mouse.get_pos()

    # Let's make a circle
    circle = pygame.draw.circle(screen, circle_color, (x, y), 50)

    if circle.collidepoint(pos):
        circle_color = LIGHT_GREEN
    elif current_rect.colliderect(circle):
        circle_color = RED
    else:
        circle_color = PINK

    text = font.render("Hello World", True, LIGHT_GREEN)

    button = Button.Button(200, 250, 200, 100, "START GAME")
    button.draw(screen)

    if button.is_clicked():
        button.visible = False
        circle_color = WHITE

    text_rect = text.get_rect(center=(WIDTH//2, LENGTH//2))

    screen.blit(text, text_rect)

    pygame.display.update()       # Updates the display so the blue is there

pygame.quit()
