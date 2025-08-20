import pygame

pygame.init()
pygame.font.init()

font = pygame.font.Font('freesansbold.ttf', 18)

"""
This class draws an interactable button in Pygame.
"""


class Button:
    def __init__(self, x, y, width, height, text,
                 text_color=(0, 0, 0),
                 color=(200, 200, 200),
                 hover_color=(150, 150, 150)):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        # Assign defaults
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color

        self.font = font

        self.visible = True

    def draw(self, screen):

        # If the button is not enabled, do not draw it on the screen!
        if not self.visible:
            return

        # Change color when hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Draw border
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Draw text centered
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # Determines whether the button has been clicked or not.
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            return True
        return False
