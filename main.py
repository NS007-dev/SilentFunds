import pygame
import sys

WIDTH, HEIGHT = 320 * 3, 180 * 3
FPS = 60
PLAYER_SPEED = 200


def main():
    pygame.init()
    pygame.display.set_caption("Silent Funds — Step 3")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # --- Player setup ---
    player = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)  # start in middle

# walls
    walls = [
        pygame.Rect(100, 100, 760, 20),   # top wall
        pygame.Rect(100, 420, 760, 20),   # bottom wall
        pygame.Rect(100, 120, 20, 300),   # left wall
        pygame.Rect(840, 120, 20, 300),   # right wall
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # time since last frame in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0  # direction of movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED * dt

# move plaer
        player.x += dx
        player.y += dy

        # wall collide
        for wall in walls:
            if player.colliderect(wall):
                player.x -= dx
                player.y -= dy
                break

        # Draw everything
        screen.fill((20, 20, 30))                   # dark blue background
        pygame.draw.rect(screen, (200, 50, 50), player)  # red player
        for wall in walls:
            pygame.draw.rect(screen, (80, 80, 120), wall)  # gray walls
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
