import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silent Funds - School Mystery")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Player setup
player = pygame.Rect(50, 200, 40, 40)
player_speed = 4

# Game state
inventory = []
current_room = "lobby"
interacting = False
active_message = None
active_choices = {}
interaction_type = None
interaction_data = None
interaction_ready = True  # cooldown for key press

# --- SCHOOL MAP ---
rooms = {
    "lobby": {
        "npcs": [],
        "clues": [],
        "doors": [{"rect": pygame.Rect(580, 200, 40, 80), "target": "hallway", "spawn": (50, 200)}]
    },
    "hallway": {
        "npcs": [pygame.Rect(300, 200, 40, 40)],
        "clues": [{"rect": pygame.Rect(200, 350, 30, 30),
                   "message": "You find a crumpled school schedule. Take it?",
                   "choices": {"1": "Take schedule", "2": "Leave it", "3": "Ignore it"},
                   "collected": False}],
        "doors": [
            {"rect": pygame.Rect(0, 200, 40, 80),
             "target": "lobby", "spawn": (540, 200)},
            {"rect": pygame.Rect(580, 150, 40, 80),
             "target": "classroom_a", "spawn": (50, 150)},
            {"rect": pygame.Rect(580, 300, 40, 80),
             "target": "cafeteria", "spawn": (50, 300)},
            {"rect": pygame.Rect(280, 0, 80, 40),
             "target": "gym", "spawn": (280, 440)},
            {"rect": pygame.Rect(
                500, 0, 80, 40), "target": "principal_office", "spawn": (100, 400)}
        ]
    },
    "classroom_a": {
        "npcs": [pygame.Rect(400, 300, 40, 40)],
        "clues": [{"rect": pygame.Rect(250, 250, 30, 30),
                   "message": "A doodle on the desk says: 'Meet me in the gym at midnight'. Take it?",
                   "choices": {"1": "Take note", "2": "Leave it", "3": "Ignore it"},
                   "collected": False}],
        "doors": [{"rect": pygame.Rect(0, 150, 40, 80), "target": "hallway", "spawn": (540, 150)}]
    },
    "classroom_b": {
        "npcs": [pygame.Rect(350, 250, 40, 40)],
        "clues": [{"rect": pygame.Rect(200, 200, 30, 30),
                   "message": "You see a shiny brass key on the desk. Take it?",
                   "choices": {"1": "Take key", "2": "Leave it", "3": "Ignore it"},
                   "collected": False}],
        "doors": [{"rect": pygame.Rect(0, 200, 40, 80), "target": "hallway", "spawn": (540, 200)}]
    },
    "cafeteria": {
        "npcs": [pygame.Rect(300, 250, 40, 40), pygame.Rect(350, 350, 40, 40)],
        "clues": [],
        "doors": [
            {"rect": pygame.Rect(0, 300, 40, 80),
             "target": "hallway", "spawn": (540, 300)},
            {"rect": pygame.Rect(580, 300, 40, 80),
             "target": "classroom_b", "spawn": (50, 200)}
        ]
    },
    "principal_office": {
        "npcs": [pygame.Rect(400, 200, 40, 40)],
        "clues": [{"rect": pygame.Rect(250, 250, 30, 30),
                   "message": "You discover a secret basement hatch. Open it?",
                   "choices": {"1": "Open hatch", "2": "Leave it", "3": "Ignore it"},
                   "collected": False}],
        "doors": [
            {"rect": pygame.Rect(100, 440, 80, 40),
             "target": "hallway", "spawn": (500, 100)},
            {"rect": pygame.Rect(300, 440, 80, 40),
             "target": "basement", "spawn": (300, 50)}
        ]
    },
    "gym": {
        "npcs": [],
        "clues": [],
        "doors": [{"rect": pygame.Rect(280, 440, 80, 40), "target": "hallway", "spawn": (280, 50)}]
    },
    "basement": {
        "npcs": [pygame.Rect(300, 300, 40, 40)],
        "clues": [{"rect": pygame.Rect(350, 350, 30, 30),
                   "message": "A ledger titled 'Silent Funds' lies here. Take it?",
                   "choices": {"1": "Take ledger", "2": "Leave it", "3": "Ignore it"},
                   "collected": False}],
        "doors": [{"rect": pygame.Rect(300, 0, 80, 40), "target": "principal_office", "spawn": (300, 400)}]
    }
}

# --- FUNCTIONS ---


def draw_text(text, x, y, color=BLACK):
    font = pygame.font.Font(None, 28)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + i * 30))


def interact_with_npc():
    global interacting, active_message, active_choices, interaction_type
    active_message = "The person looks at you suspiciously...\n1. Ask about rumors\n2. Stay quiet\n3. Leave"
    active_choices = {"1": "They whisper: 'Check the gym at night.'",
                      "2": "They ignore you.", "3": "You walk away."}
    interaction_type = "npc"
    interacting = True


def interact_with_clue(clue):
    global interacting, active_message, active_choices, interaction_type, interaction_data
    active_message = clue["message"]
    active_choices = clue["choices"]
    interaction_type = "clue"
    interaction_data = clue
    interacting = True


def process_choice(choice):
    global interacting, active_message, inventory, interaction_data
    if choice in active_choices:
        response = active_choices[choice]
        if interaction_type == "npc":
            active_message = response
        elif interaction_type == "clue":
            active_message = response
            if choice == "1" and not interaction_data["collected"]:
                inventory.append(response.split()[1])
                interaction_data["collected"] = True
    else:
        active_message = "Invalid choice."
    if choice == "3":
        interacting = False


# --- MAIN LOOP ---
running = True
while running:
    clock.tick(30)
    screen.fill(WHITE)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and interacting:
            if event.unicode in active_choices:
                process_choice(event.unicode)

    # Player movement
    if not interacting:
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_UP]:
            player.y -= player_speed
        if keys[pygame.K_DOWN]:
            player.y += player_speed

    # Interaction cooldown reset
    if not keys[pygame.K_e]:
        interaction_ready = True

    # Keep player inside screen
    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(0, min(HEIGHT - player.height, player.y))

    room = rooms[current_room]

    # NPC interaction
    for npc in room["npcs"]:
        if not hasattr(npc, "interacted"):
            npc.interacted = False
        pygame.draw.rect(screen, BLUE, npc)
        if player.colliderect(npc) and keys[pygame.K_e] and not interacting and not npc.interacted and interaction_ready:
            interact_with_npc()
            npc.interacted = True
            interaction_ready = False

    # Clue interaction
    for clue in room["clues"]:
        if not hasattr(clue, "interacted"):
            clue.interacted = False
        if not clue["collected"]:
            pygame.draw.rect(screen, GREEN, clue["rect"])
        if player.colliderect(clue["rect"]) and keys[pygame.K_e] and not interacting and not clue.interacted:
            interact_with_clue(clue)
            clue.interacted = True
            interaction_ready = False

    # Door interaction
    for door in room["doors"]:
        pygame.draw.rect(screen, RED, door["rect"])
        if player.colliderect(door["rect"]) and not interacting:
            current_room = door["target"]
            player.topleft = door["spawn"]

    # Draw player
    pygame.draw.rect(screen, BLACK, player)

    # Interaction box
    if interacting:
        pygame.draw.rect(screen, WHITE, (50, 350, 540, 120))
        pygame.draw.rect(screen, BLACK, (50, 350, 540, 120), 2)
        draw_text(active_message, 60, 360)

    # Inventory display
    draw_text("Inventory: " + ", ".join(inventory), 10, 10)

    pygame.display.flip()

pygame.quit()
sys.exit()
