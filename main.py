import pygame
import sys

WIDTH, HEIGHT = 320 * 3, 180 * 3
FPS = 60
PLAYER_SPEED = 200


def main():
    pygame.init()
    pygame.display.set_caption("Silent Funds — Step 9")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24)

    player = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)

    walls = [
        pygame.Rect(100, 100, 760, 20),
        pygame.Rect(100, 420, 760, 20),
        pygame.Rect(100, 120, 20, 300),
        pygame.Rect(840, 120, 20, 300),
    ]

    # --- Choices memory ---
    player_choices = {}  # stores what the player picked

    # --- Clues ---
    clues = [
        {
            "rect": pygame.Rect(200, 200, 20, 20),
            "message": "A torn note lies here. What will you do?",
            "choices": {
                "1": "Read it carefully.",
                "2": "Pocket it quickly.",
                "3": "Ignore it."
            },
            "id": "note",
            "collected": False
        },
        {
            "rect": pygame.Rect(600, 250, 20, 20),
            "message": "You find a key on the ground. Action?",
            "choices": {
                "1": "Take the key.",
                "2": "Leave it.",
                "3": "Look around suspiciously."
            },
            "id": "key",
            "collected": False
        },
    ]

    npc = {
        "rect": pygame.Rect(400, 300, 40, 60),
        "name": "Mysterious Stranger",
        "dialogue": "I saw what you did earlier...",
        "followup": {
            "note": {
                "Read it carefully.": "So, you like details... be cautious.",
                "Pocket it quickly.": "Greedy, huh? That might cost you later.",
                "Ignore it.": "Strange... ignoring clues won't save you."
            },
            "key": {
                "Take the key.": "Keys open doors... or trouble.",
                "Leave it.": "Sometimes leaving things is wise.",
                "Look around suspiciously.": "Paranoia is healthy here."
            }
        }
    }

    current_message = None
    current_choices = None
    choice_result = None
    talking_to_npc = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.KEYDOWN and current_choices:
                if event.unicode in current_choices:
                    choice_result = current_choices[event.unicode]
                    current_message = f"You chose: {choice_result}"
                    player_choices[active_id] = choice_result  # save choice
                    current_choices = None

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if current_message and not current_choices:
                    current_message = None
                    choice_result = None
                    talking_to_npc = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if not current_message:  # stop movement during dialogue
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -PLAYER_SPEED * dt
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED * dt
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -PLAYER_SPEED * dt
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = PLAYER_SPEED * dt

        player.x += dx
        player.y += dy

        for wall in walls:
            if player.colliderect(wall):
                player.x -= dx
                player.y -= dy
                break

        for clue in clues:
            if not clue["collected"] and player.colliderect(clue["rect"]):
                clue["collected"] = True
                current_message = clue["message"]
                current_choices = clue["choices"]
                active_id = clue["id"]

        if player.colliderect(npc["rect"]) and not talking_to_npc:
            talking_to_npc = True
            current_message = npc["dialogue"]

            for clue_id, result in player_choices.items():
                if clue_id in npc["followup"] and result in npc["followup"][clue_id]:
                    current_message = npc["followup"][clue_id][result]
                    break  # first relevant response wins

        screen.fill((20, 20, 30))
        pygame.draw.rect(screen, (200, 50, 50), player)
        for wall in walls:
            pygame.draw.rect(screen, (80, 80, 120), wall)
        for clue in clues:
            if not clue["collected"]:
                pygame.draw.rect(screen, (240, 230, 100), clue["rect"])
        pygame.draw.rect(screen, (50, 200, 50), npc["rect"])  # NPC visible

        if current_message:
            box = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 130)
            pygame.draw.rect(screen, (0, 0, 0), box)
            pygame.draw.rect(screen, (255, 255, 255), box, 3)

            text = font.render(current_message, True, (255, 255, 255))
            screen.blit(text, (box.x + 15, box.y + 15))

            if current_choices:  # list all options
                y_offset = 50
                for key, option in current_choices.items():
                    option_text = font.render(
                        f"{key}: {option}", True, (200, 200, 200))
                    screen.blit(option_text, (box.x + 15, box.y + y_offset))
                    y_offset += 30

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
