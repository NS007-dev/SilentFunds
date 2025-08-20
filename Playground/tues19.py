import pygame
pygame.init()

WIDTH = 600
LENGTH = 600


screen = pygame.display.set_mode((WIDTH, LENGTH))    # determines screen size
pygame.display.set_caption("My first game")     # Window title

x = 100
y = 100

player_left = pygame.image.load("walk_left.png")
player_left = pygame.transform.scale_by(player_left, 2)
player_right = pygame.image.load("walk_right.png")
player_right = pygame.transform.scale_by(player_right, 2)
player_up = pygame.image.load("walk_up.png")
player_up = pygame.transform.scale_by(player_up, 2)
player_down = pygame.image.load("walk_left.png")
player_down = pygame.transform.scale_by(player_left, 2)

current_sprite = player_left


# Predefined colors
LIGHT_GREEN = (181, 238, 174)
LIGHT_BLUE = (100, 150, 200)
PINK = (227, 165, 192)
RED = (180, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = pygame.time.Clock()
framerate = 60

running = True
while running:

    FPS.tick(framerate)

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:   # Determine if the user hit quit
            running = False

    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_DOWN] and y + 50 < LENGTH:
        print("down")
        y = y + 10
        current_sprite = player_up
    if user_input[pygame.K_UP] and y - 50 > 0:
        print("up")
        y = y - 10
        current_sprite = player_up
    if user_input[pygame.K_LEFT] and x - 50 > 0:
        print("left")
        x = x - 10
        current_sprite = player_left
    if user_input[pygame.K_RIGHT] and x + 50 < WIDTH:
        print("RIGHT")
        x = x + 10
        current_sprite = player_right

    screen.fill(LIGHT_BLUE)  # Fills the screen with a light blue background!

    # Let's make a rectangle
    my_rectangle = pygame.Rect(100, 200, 200, 100)
    pygame.draw.rect(screen, RED, my_rectangle)

# create sprite
    screen.blit(current_sprite, (x, y))

    pygame.display.update()       # Updates the display so the blue is there

pygame.quit()
