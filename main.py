# main.py — Step 2: add a player square that moves

import pygame
import sys

# --- Config ---
WIDTH, HEIGHT = 320 * 3, 180 * 3
FPS = 60
PLAYER_SPEED = 200  # pixels per second


def main():
    pygame.init()
    pygame.display.set_caption("Silent Funds — Step 2")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # --- NEW: player setup ---
    player = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)  # x, y, w, h

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Input / events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- NEW: movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= PLAYER_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += PLAYER_SPEED * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= PLAYER_SPEED * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += PLAYER_SPEED * dt

        # --- Draw ---
        screen.fill((12, 12, 16))
        # NEW: draw player square
        pygame.draw.rect(screen, (200, 50, 50), player)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
