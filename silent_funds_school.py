import pygame
import sys  # for the system
import string  # for the words

pygame.init()


WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silent Funds")
clock = pygame.time.Clock()  # game speed

#  generate colors, do i need to hand write out the colourss or isnt there built in?

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (35, 35, 35)
RED = (200, 60, 60)
GREEN = (60, 160, 80)
BLUE = (60, 110, 220)
YELLOW = (230, 200, 60)
TEAL = (60, 190, 190)
PURPLE = (150, 80, 190)
BROWN = (120, 90, 60)

FONT = pygame.font.SysFont(None, 22)
BIG = pygame.font.SysFont(None, 36)
TITLE = pygame.font.SysFont(None, 44)

# no specific font used


def draw_text(text, x, y, font=FONT, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# draws the one line of text at x,y in the specific font and colour
# render converts the text into image to be drawn
# blit draws the image on screen


def draw_text_wrapped(text, x, y, max_width, line_height=22, color=BLACK):
    words = text.split()  # splits a string into array of words
    line = ""
    cy = y  # current y position
    for w in words:  # loop thru workds one word at a time, w is current.
        # add current word to sentence, .strip remvoed spaces
        test = (line + " " + w).strip()
        # makes text into image, using font colour and smooth
        img = FONT.render(test, True, color)
        if img.get_width() > max_width and line:
            screen.blit(FONT.render(line, True, color), (x, cy))
            cy += line_height  # if text is too wide then start new line
            line = w
        else:
            # otherwise keep adding to that line if it fits max width.
            line = test
    if line:
        screen.blit(FONT.render(line, True, color), (x, cy))
        # whatever remains also add that as a seperate line

# splits text if its too longinto seperate times, max_width the max with of line before breaking it


player = pygame.Rect(140, 220, 36, 36)
PLAYER_SPEED = 4

# the player, so far in rectangle form, need an image sprite
# player starting position and size
# players frame speed


# Name input
player_name = "Enola"
input_name = player_name
game_mode = "name_entry"  # tracks if the player enters their name

# STORY STARTS:

evidence_points = 0  # The evidence tracker
ally_john = False  # john not ally at start
john_boost_from_stage = 4   # John's +1 boost when reached stage 4
story_stage = 1             # chapters of stort up to 6
# marks and holds specific events and milestones, remember what youvee done
visited_flags = set()

# Interaction & dialog state
interacting = False
active_title = ""  # will be filled with text
active_text = ""
active_choices = {}   # will hold array of players choices
active_payload = None
active_clue_ref = None

# avoiding retriggers
interaction_ready = True
exit_cooldown = 0

# ROOMS:

rooms = {
    "gym": {
        # IMAGE HERE: gymbackground in draw_room()
        "bg": None,  #  image?
        "doors": [  #  door is rectangle, with its position and dimensions,
            {"rect": pygame.Rect(880, 240, 60, 160),
             "target": "hallway", "spawn": (80, 300)}
            # if you go thur it takes you to hallway
            # you will spawn into that position in hallway
        ],
        "npcs": [  # so far eahc npc is a rectangle. default false interaction
            {"name": "Jamie", "rect": pygame.Rect(
                280, 300, 40, 40), "color": TEAL, "interacted": False},
            {"name": "Coach Ramirez", "rect": pygame.Rect(
                520, 260, 40, 40), "color": BLUE, "interacted": False}
        ],
        "clues": [
            # scene1 is initiated automatically at start
        ]
    },
    "hallway": {
        "bg": None,  # IMAGE?
        "doors": [  # all the doors.
            {"rect": pygame.Rect(0, 240, 60, 160),
             "target": "gym", "spawn": (760, 300)},
            {"rect": pygame.Rect(420, 0, 120, 60),
             "target": "principal_office", "spawn": (460, 520)}
        ],
        "npcs": [
            {"name": "Mr. Patel", "rect": pygame.Rect(
                260, 240, 40, 40), "color": PURPLE, "interacted": False},
            # Janitor John will be appended later when scene 4 triggers
        ],
        "clues": [  # clues with descrips
            {"key": "public_docs", "rect": pygame.Rect(700, 310, 28, 28), "color": YELLOW,
             "message": "Public records: pages of donation records. These are complicated but show irregularities.",
             "choices": {"1": "Take notes", "2": "Leave it"}, "collected": False, "interacted": False, "shown": True}
        ]
    },
    "principal_office": {
        "bg": None,
        "doors": [
            {"rect": pygame.Rect(420, 560, 120, 64),
             "target": "hallway", "spawn": (460, 80)}
        ],
        "npcs": [
            {"name": "Principal Wallaker", "rect": pygame.Rect(
                300, 220, 40, 40), "color": RED, "interacted": False},
            {"name": "Ms. Larkin", "rect": pygame.Rect(
                520, 220, 40, 40), "color": GREEN, "interacted": False}
        ],
        "clues": [
            {"key": "hatch", "rect": pygame.Rect(260, 320, 28, 28), "color": BROWN,
             "message": "A hatch to a lower level. Could be important.",
             "choices": {"1": "Open hatch", "2": "Leave it"}, "collected": False, "interacted": False, "shown": True}
        ]
    },
    "basement": {
        # basement is entered from inside principal_office hatch (we'll gate it)
        "bg": None,
        "doors": [
            {"rect": pygame.Rect(440, 0, 120, 48),
             "target": "principal_office", "spawn": (460, 500)}
        ],
        "npcs": [
            {"name": "Mysterious Figure", "rect": pygame.Rect(
                300, 300, 40, 40), "color": DARK, "interacted": False}
        ],
        "clues": [
            {"key": "ledger", "rect": pygame.Rect(350, 350, 36, 36), "color": TEAL,
             "message": "Ledger titled 'Silent Funds' — detailed entries about missing donations.",
             "choices": {"1": "Take ledger", "2": "Leave it"}, "collected": False, "interacted": False, "shown": True}
        ]
    }
}
current_room = "gym"


# global interacting updates game state across entireee program not just this function
def open_dialog(title, text, choices=None, payload=None):
    global interacting, active_title, active_text, active_choices, active_payload
    active_title = title
    active_text = text
    active_choices = choices or {}
    active_payload = payload or {}
    # shows what to store the current said text and what choices availavble default empty or {} if nothing
    interacting = True
    # pause gameplay if interacting.


def close_dialog():  # when ending dialog
    global interacting, exit_cooldown  #  make sure its tracked thru all game
    interacting = False
    exit_cooldown = 16  # small frames cooldown to avoid immediate retrigger


def add_points(base):
    global evidence_points
    boost = 1 if (ally_john and story_stage >= john_boost_from_stage) else 0
    evidence_points += base + boost
    # if john is true and story stage matches the john +1 stage then yeah add boost.


# make sure janitor is added to right point
def ensure_john_spawned():
    hall = rooms["hallway"]
    # searches thru all npcs in the hallway if any matches to john stop bc you dont want duplicates.
    for npc in hall["npcs"]:
        if npc.get("name") == "Janitor John":
            return
    # Janitor John position: (120,360) — IMAGE OF HIM
    hall["npcs"].append({"name": "Janitor John", "rect": pygame.Rect(
        120, 360, 40, 40), "color": BLUE, "interacted": False})
    #  this is if hes missing


def handle_scene1_intro():  #  scene 1
    if "scene1_opened" in visited_flags:  # checks if ive already viisted scene1
        return
    # f string insert var into string \n newline
    visited_flags.add("scene1_opened")
    text = (f"Gym — Charity night.\n\nJamie: \"{player_name}, the donation totals announced here don't match what's posted online. "
            "Something's wrong.\"\n\nYou decide to investigate.")
    open_dialog("ACT 1 — Something's Wrong", text, {
                "1": "Okay"}, payload={"scene": "scene1_ack"})


# NPC interactionsss so global stroy_stage = they are all saved for thru out game
def npc_interact(name):
    global story_stage
    # JAMIE
    if name == "Jamie":
        if story_stage == 1:
            open_dialog("Jamie", f"Jamie: \"I noticed the totals don't match online, {player_name}. We should look into it.\"",
                        {"1": "I'll investigate"}, payload={"flag": "talked_jamie"})
            return
        else:
            open_dialog(
                "Jamie", "Jamie looks nervous and keeps distance.", {"1": "…"})
            return

    # PRINCIPAL WALLAKER
    if name == "Principal Wallaker":
        if story_stage <= 2 and "s2_wallaker_done" not in visited_flags:
            text = (
                f"Principal Wallaker: \"Sweetie, I'm sure you mean well, but maybe this is... too complex for a young lady like you to understand, {player_name}.\"")
            open_dialog("Principal Wallaker", text, {"1": "…"}, payload={
                        "grant_points": 1, "flag": "s2_wallaker_done", "advance_to": 3})
            return
        else:
            open_dialog("Principal Wallaker",
                        "Everything is under control here.", {"1": "Leave"})
            return

    # Mr. PATEL
    if name == "Mr. Patel":
        if story_stage <= 2 and "s2_patel_done" not in visited_flags:
            text = ("Mr. Patel (Accountant) looks nervous: \"Some donations aren't processed normally... "
                    "They don't listen to people like us, especially not young women.\"")
            open_dialog("Mr. Patel", text, {"1": "Thank you"}, payload={
                        "grant_points": 3, "flag": "s2_patel_done", "advance_to": 3})
            return
        else:
            open_dialog("Mr. Patel", "I... shouldn't say more.",
                        {"1": "Leave"})
            return

    # COACH RAMIREZ
    if name == "Coach Ramirez":
        if story_stage <= 2 and "s2_ramirez_done" not in visited_flags:
            text = ("Coach Ramirez: \"Stay away from Ms. Larkin. Be careful, kid. They already think you're trouble, "
                    "and girls like you... they don't give second chances.\"")
            open_dialog("Coach Ramirez", text, {"1": "Got it"}, payload={
                        "grant_points": 2, "flag": "s2_ramirez_done", "advance_to": 3})
            return
        else:
            open_dialog("Coach Ramirez",
                        "Focus on staying safe.", {"1": "Leave"})
            return

    # JANITOR JOHN
    if name == "Janitor John":
        if "s4_john_joined" not in visited_flags:
            text = ("Janitor John: \"I've seen stuff, but nobody listens to the janitor. Maybe they'll listen to you. I got your back.\"")
            open_dialog("Janitor John", text, {"1": "Thanks"}, payload={
                        "ally_john": True, "flag": "s4_john_joined"})
            return
        else:
            open_dialog("Janitor John", "I'll back you. Keep gathering proof.", {
                        "1": "Thanks"})
            return

    # MS. LARKIN
    if name == "Ms. Larkin":
        if story_stage < 5:
            open_dialog("Ms. Larkin", "…Can I help you?", {"1": "Leave"})
            return
        elif story_stage == 5:
            text = ("Ms. Larkin: \"Honey, I think you're being a little too emotional about this. Maybe you're seeing problems that aren't there.\"")
            open_dialog("Ms. Larkin", text, {
                        "1": "…"}, payload={"advance_to": 6})
            return
        elif story_stage == 6:
            text = ("Evidence points to Ms. Larkin.\n\nFinal Choice:")
            choices = {
                "1": "Do nothing (0 pts)",
                "2": "Confront Ms. Larkin (2 pts)",
                "3": "Report to police (3 pts)"
            }
            open_dialog("ACT 5–6 — The Truth", text,
                        choices, payload={"final": True})
            return


# when key is gound for the principles office, and all the dialogue
def clue_interact(key):
    # only public_docs and ledger/hatch/ etc in our map
    if key == "public_docs":
        if story_stage == 3 and "s3_docs_done" not in visited_flags:
            text = ("Clerk: \"These are complicated financial documents. Maybe ask your father to help explain them?\"\n\n"
                    "You study the public records and spot irregularities.")
            open_dialog("Public Documents", text, {"1": "Take notes"}, payload={
                        "grant_points": 3, "flag": "s3_docs_done"})
        else:
            open_dialog("Public Documents", "Just more stacks of reports. Nothing new.", {
                        "1": "Leave"})
    elif key == "hatch":
        # hatch should only be available if player has the brass key in inventory
        # We'll check inventory thru  active_payload or direct flagm we store key as visited_flags "have_key"
        if "have_key" in visited_flags:
            open_dialog("Basement Hatch", "The hatch is unlocked. Open it to go down?", {
                        "1": "Open hatch", "2": "Leave"}, payload={"open_hatch": True})
        else:
            open_dialog("Basement Hatch",
                        "The hatch is locked. You need a key.", {"1": "Leave"})
    elif key == "ledger":
        if story_stage >= 5:
            open_dialog("Ledger", "This ledger documents diverted donations. This is the smoking gun.", {
                        "1": "Take ledger"}, payload={"grant_points": 3, "flag": "got_ledger"})
        else:
            open_dialog("Ledger", "Old ledger. Read later.", {"1": "Leave"})

# After closing dialogs, progress scenes


def maybe_progress_story():  # cgecks flags to see if we should progress
    global story_stage
    # Advance from stage2 to  3 if any scene2 talk happened
    if story_stage == 2:
        if any(f in visited_flags for f in ("s2_wallaker_done", "s2_patel_done", "s2_ramirez_done")):
            story_stage = 3

            # make sure i have interacted with npc before letting me move on to part 3

    # Present Scene 3 choice once
    if story_stage == 3 and "s3_presented_choice" not in visited_flags:
        visited_flags.add("s3_presented_choice")
        text = ("Staff go quiet when you walk by. Students whisper:\n"
                "• 'She’s just being dramatic'\n• 'She always makes everything about race'\n"
                "• 'Why can't she just be quiet like other girls?'\n• 'She's too aggressive'\n\nWhat do you do?")
        open_dialog("ACT 2 — Getting Clues", text, {
                    "1": "Talk to more staff (2 pts)", "2": "Look at public documents (3 pts)"}, payload={"scene3_choice": True})
        return

    # If scene3 resolved, create John event and advance to stage4
    if story_stage == 3 and "s3_resolved" in visited_flags and "s4_ready" not in visited_flags:
        visited_flags.add("s4_ready")
        story_stage = 4
        ensure_john_spawned()
        open_dialog("ACT 3 — Getting Help",
                    "A note appears in your locker: 'Meet me after school.' Find Janitor John in the hallway.", {"1": "Okay"})
        return

    # Stage 4 -> 5 when Janitor joined
    if story_stage == 4 and "s4_john_joined" in visited_flags and "s5_presented" not in visited_flags:
        visited_flags.add("s5_presented")
        story_stage = 5
        open_dialog("ACT 4 — Pressure",
                    "Friends start to avoid you. Jamie distances himself.", {"1": "…"})
        return


#  what happens when player picks a choice:

def on_choice_selected(choice):
    global story_stage, ally_john, evidence_points
    payload = active_payload or {}

    # choices 1 2 or 3, playload carries all the instructions on what choice will do .

    # generic grants
    if "grant_points" in payload:
        add_points(payload["grant_points"])
    if "flag" in payload:
        visited_flags.add(payload["flag"])
    if payload.get("advance_to"):
        story_stage = max(story_stage, payload["advance_to"])
    if payload.get("ally_john"):
        ally_john = True

        # iff payload says grant points, then csll addpoints function
        # flag means record it into events that should be remembered
        # advnace to = move story
        # ally john = join the player
    if payload.get("open_hatch"):
        # Move player to basement immediately
        open_dialog("Basement", "You open the hatch and climb down.", {
                    "1": "Continue"}, payload={"go_to_basement": True})
        return

        # open hatch present means show new dialog and mark basement.

    # Scene1
    if payload.get("scene") == "scene1_ack":
        story_stage = 2
        return
    # move to stage 2

    # Scene3 choice
    if payload.get("scene3_choice"):
        if choice == "1":
            # Talk to staff (condescending) -> +2
            open_dialog("Staff (condescending)", "'Are you sure you’re not just… being emotional about this, honey?'", {
                        "1": "…"}, payload={"grant_points": 2, "flag": "s3_resolved"})
            return
        elif choice == "2":
            open_dialog("Records Clerk", "'These are complicated. Maybe ask your father.'", {
                        "1": "Review documents"}, payload={"grant_points": 3, "flag": "s3_resolved"})
            return

        # option 1: talk to staff = 2pts
        # option 2: review records, 3pts
        # then in flags mark as resolved.

    # Final choice payloads
    if payload.get("final"):
        if choice == "1":
            end_game(added=0, mode="do_nothing")
            return
        elif choice == "2":
            open_dialog("Confrontation", "Ms. Larkin: 'Sweetheart, you're just a young girl getting worked up over nothing.'", {
                        "1": "…"}, payload={"final_confront": True})
            return
        elif choice == "3":
            open_dialog("Police", "Officer: 'Are you sure this isn't high school girl drama?'", {
                        "1": "Submit report"}, payload={"final_report": True})
            return

        # choice 1: nothing choice 2: confront authority 3: go to police

    if payload.get("final_confront"):
        end_game(added=2, mode="confront")  # 2 points add
        return
    if payload.get("final_report"):
        # police will act only if enough evidence, 3 points add
        end_game(added=3, mode="report")
        return

    # Special actions
    if payload.get("go_to_basement"):
        # switch rooms special room
        change_room("basement")
        return

# Compute endings


def end_game(added, mode):
    add_points(added)
    total = evidence_points
    if total >= 6:
        title = "Justice Ending"
        text = "Ms. Larkin gets caught. Some still blame you for causing drama, but truth wins."
    elif 3 <= total <= 5:
        title = "Partial Justice Ending"
        text = "An investigation starts but is slow. You moved things forward."
    else:
        title = "Failure Ending"
        text = "Not enough evidence. Corruption continues; you learn how hard speaking up is."
    open_dialog(title, f"Final Evidence: {total}\n\n{text}\n\n(Press E to return to title)", payload={
                "game_over": True})

    # add points is all the evidence, then its totalled
    # total is greated than or = to 6, tjen justice
    # total is bigger than 3 but less than 5 then partial justsice
    # less than 3 then failed


def reset_to_title():
    global evidence_points, ally_john, story_stage, visited_flags, current_room
    global interacting, active_title, active_text, active_choices, active_payload
    global player, game_mode, input_name, player_name
    evidence_points = 0
    ally_john = False
    story_stage = 1
    visited_flags = set()
    current_room = "gym"
    player.topleft = (140, 220)
    interacting = False
    active_title = active_text = ""
    active_choices = {}
    active_payload = None
    game_mode = "name_entry"
    input_name = player_name

    # resets everythningggg back to the start and clears memory


def change_room(room_name):
    global current_room, player
    current_room = room_name
    # set sensible spawn positions per room
    if room_name == "gym":
        player.topleft = (140, 220)
    elif room_name == "hallway":
        player.topleft = (200, 300)
    elif room_name == "principal_office":
        player.topleft = (460, 400)
    elif room_name == "basement":
        player.topleft = (240, 300)

    # this sets all the positions and scenes


def draw_room():
    # replace rectangles with images.
    room = rooms[current_room]
    # Background placeholder
    screen.fill(GRAY)
    # ASSET blit here using room["bg"].

    # Doors
    for d in room["doors"]:
        pygame.draw.rect(screen, (120, 200, 120), d["rect"])
        # ASSET: blit(door_sprite, d["rect"].topleft)

    # Clues
    for clue in room.get("clues", []):
        if clue.get("shown", True) and not clue.get("collected", False):
            pygame.draw.rect(screen, clue["color"], clue["rect"])
            # ASSET: blit(clue_sprite, clue["rect"].topleft)

    # NPCs
    for npc in room.get("npcs", []):
        pygame.draw.rect(screen, npc["color"], npc["rect"])
        # ASSET: blit(npc_sprite, npc["rect"].topleft)


def draw_hud():
    # the bar at the top.
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 72))
    # the backgrounf
    pygame.draw.line(screen, BLACK, (0, 72), (WIDTH, 72), 2)
    #  separate
    screen.blit(TITLE.render(player_name, True, BLACK), (12, 8))
    # player name
    screen.blit(BIG.render(
        f"Room: {current_room.title().replace('_', ' ')}", True, BLACK), (220, 8))
    # room name
    screen.blit(BIG.render(
        f"Evidence: {evidence_points}", True, BLACK), (520, 8))
    ally_status = "Yes" if ally_john else "No"
    screen.blit(BIG.render(f"Ally John: {ally_status}", True, BLACK), (700, 8))
    draw_text(
        "Move: Arrows/WASD • Interact: E • Choose: 1/2/3 • Exit dialog: E", 12, 48)


def draw_panel(title, text, choices=None):
    pygame.draw.rect(screen, WHITE, (48, 364, 864, 260))
    pygame.draw.rect(screen, BLACK, (48, 364, 864, 260), 2)
    screen.blit(BIG.render(title, True, BLACK), (64, 372))
    draw_text_wrapped(text, 64, 412, max_width=820)
    if choices:
        y = 488
        for k, v in choices.items():
            draw_text(f"{k}: {v}", 64, y)
            y += 28
    draw_text("(Press number to choose, or E to close)", 64, 612)
 # the dialogue panel


booted = False

while True:  # game running until quit
    if game_mode == "name_entry":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # window closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # save name
                    player_name = input_name.strip() or player_name
                    game_mode = "play"
                    booted = False
                    # reset story state
                    evidence_points = 0
                    ally_john = False
                    story_stage = 1
                    visited_flags = set()
                    current_room = "gym"
                    player.topleft = (140, 220)
                    interacting = False
                    active_title = active_text = ""
                    active_choices = {}
                    active_payload = None
                elif event.key == pygame.K_BACKSPACE:  # delete last character
                    input_name = input_name[:-1]
                else:
                    ch = event.unicode
                    allowed = string.ascii_letters + string.digits + " -'"
                    if ch in allowed and len(input_name) < 24:
                        input_name += ch

                    # adds name onlyyy iffff letters nums spaces, dashes apostrophe length is less than or equal to 24

        # draw name screen
        screen.fill(DARK)
        screen.blit(TITLE.render(
            "Silent Funds — School Mystery", True, WHITE), (64, 64))
        draw_text_wrapped("You’re the only member of the school newspaper — a young woman of color in a mostly white school. "
                          "People underestimate you. Type your name and press Enter to begin.", 80, 160, max_width=760, color=WHITE)
        pygame.draw.rect(screen, WHITE, (80, 280, 560, 56))
        pygame.draw.rect(screen, BLACK, (80, 280, 560, 56), 2)
        shown = input_name + \
            ("|" if (pygame.time.get_ticks()//500) % 2 == 0 else "")
        screen.blit(BIG.render(shown, True, BLACK), (94, 288))
        draw_text("Press Enter to start", 80, 360, font=FONT, color=WHITE)
        pygame.display.flip()
        clock.tick(60)
        continue

    # PLAY MODE
    if not booted:
        booted = True
        handle_scene1_intro()

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if interacting:
                # number choice
                if event.unicode in active_choices:
                    # apply generic payload first if any (delayed handling in on_choice_selected)
                    # mark visited flags / grants immediately
                    if active_payload:
                        if "grant_points" in active_payload:
                            add_points(active_payload["grant_points"])
                        if "flag" in active_payload:
                            visited_flags.add(active_payload["flag"])
                        if active_payload.get("ally_john"):
                            ally_john = True
                        if active_payload.get("advance_to"):
                            story_stage = max(
                                story_stage, active_payload["advance_to"])
                    # call final handler
                    # Note: Some choices open follow-up dialogs inside on_choice_selected
                    on_choice_selected(event.unicode)
                    # If after handler there is no active dialog set, close
                    # (handlers may open new dialog)
                elif event.key == pygame.K_e:
                    # If game_over present in payload / visited_flags, reset to title
                    if active_payload and active_payload.get("game_over"):
                        reset_to_title()
                    else:
                        close_dialog()
                        maybe_progress_story()

    # MOVE (disabled while interacting)
    keys = pygame.key.get_pressed()
    if not interacting:
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - \
            (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - \
            (keys[pygame.K_UP] or keys[pygame.K_w])
        player.x += dx * PLAYER_SPEED
        player.y += dy * PLAYER_SPEED

    # clamp player
    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(72, min(HEIGHT - player.height, player.y))  # keep below HUD

    # DRAW ROOM
    draw_room()
    draw_hud()
    # ASSET: replace with player blit
    pygame.draw.rect(screen, BLACK, player)

    # DOORS: auto-transition when walking through
    for door in rooms[current_room]["doors"]:
        # door rect drawn in draw_room()
        if not interacting and exit_cooldown == 0 and player.colliderect(door["rect"]):
            change_room(door["target"])

    # NPC INTERACTIONS: press E while overlapping
    for npc in rooms[current_room]["npcs"]:
        if (not interacting) and (exit_cooldown == 0) and (keys[pygame.K_e] and interaction_ready) and player.colliderect(npc["rect"]):
            interaction_ready = False
            # specific NPC logic
            npc_interact(npc["name"])
            # mark interacted to avoid spamming (NPC dict has "interacted")
            npc["interacted"] = True

    # CLUE INTERACTIONS
    for clue in rooms[current_room]["clues"]:
        if clue.get("shown", True) and (not clue.get("collected", False)):
            if (not interacting) and (exit_cooldown == 0) and (keys[pygame.K_e] and interaction_ready) and player.colliderect(clue["rect"]) and not clue.get("interacted", False):
                interaction_ready = False
                clue_interact(clue["key"])
                clue["interacted"] = True

    # reset E readiness when released
    if not keys[pygame.K_e]:
        interaction_ready = True

    # draw interactions panel if open
    if interacting:
        draw_panel(active_title, active_text, active_choices)

    # small cooldown tick
    if exit_cooldown > 0:
        exit_cooldown -= 1

    # auto-progress story when not in dialog
    if not interacting:
        maybe_progress_story()

    #  redraw already done above, but we might want to show inventory/items:
    # Inventory area (top-right) shows which items you have (key, ledger, schedule)
    inv_texts = []
    if "have_key" in visited_flags:
        inv_texts.append("Brass Key")
    if "got_ledger" in visited_flags:
        inv_texts.append("Ledger")
    if "s3_docs_done" in visited_flags:
        inv_texts.append("Public Docs Notes")
    # draw inventory
    draw_text("Inventory:", 720, 72)
    y = 96
    for it in inv_texts:
        draw_text("- " + it, 720, y)
        y += 20

    # Final: instructions footer
    draw_text(
        "(Tip: Press E to interact. Press E again to close dialog.)", 16, HEIGHT-26)

    pygame.display.flip()
    clock.tick(60)
