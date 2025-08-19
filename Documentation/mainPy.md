import pygame, sys


Pygame = library to make game.
Sys = cleanly quit program using sys.exit()


WIDTH, HEIGHT = 320 * 3, 180 * 3
FPS = 60
PLAYER_SPEED = 200


Window size, with player speed (so sprite moves 200px per sec) and FPS which is how many times per sec game updates, in this case, 60 is smooth.

pygame.init()
pygame.display.set_caption("Silent Funds -- Step 2")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


Line 1: starts pygame
Line 2: the window title
Line 3: sets the width and height of window
Line 4: keeps track of time and the fps.

player = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)


Makes rectangle/player at centre of screen at 40x40 pixels size.

keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    player.x -= PLAYER_SPEED * dt


Function get_pressed() shows keys being currently held and what direction to move

screen.fill((12, 12, 16))
pygame.draw.rect(screen, (200, 50, 50), player)
pygame.display.flip()


.fill is for the background, then ,draw is the character, then .flip() is to update screen
