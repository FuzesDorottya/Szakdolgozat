import pygame
import os

from scripts.utilities import image
from game import Game

class Levels:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.clock = pygame.time.Clock()

        self.back_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 45)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", 50)
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.buttons = []
        self.buttons_rect()
    
    def buttons_rect(self):
        for level in range(len(os.listdir("assets/maps"))):
            gap = 40
            button_size = 100
            columns = 5
            grid_width = (columns * button_size) + ((columns - 1) * gap)
            start_x = (self.display.get_width() - grid_width) / 2
            start_y = 250
            column = level % columns
            row = level // columns
            button_x_position = start_x + column * (button_size + gap)
            button_y_position = start_y + row * (button_size + gap)
            button_rect = pygame.Rect(button_x_position, button_y_position, button_size, button_size)

            text = self.secondary_font.render(f"{level+1}", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            
            self.buttons.append((button_rect, level, text, text_rect))
    
    def run(self):
        self.running = True
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())

        levels_text = self.main_font.render("levels", True, (65, 65, 65))
        levels_text_rect = levels_text.get_rect(center=(self.display.get_width() / 2, 100))
        back_button_rect = pygame.Rect(20, 20, 150, 80)
        back_text = self.back_font.render("back", True, (65, 65, 65))
        back_text_rect = back_text.get_rect(center=(back_button_rect.centerx, back_button_rect.centery - 5))
       
        while self.running:
            self.display.blit(bgr, (0, 0))
            self.display.blit(levels_text, levels_text_rect)
            mouse_pos = pygame.mouse.get_pos()

            back_button_color = (55, 200, 100)
            back_hover_color = (35, 180, 75)
            if back_button_rect.collidepoint(mouse_pos):
                back_button_color = back_hover_color

            pygame.draw.rect(self.display, back_button_color, back_button_rect,border_radius=150)
            pygame.draw.rect(self.display, (100, 100, 100), back_button_rect, 5 ,border_radius=150)

            for button_rect, level, text, text_rect in self.buttons:
                button_color = (55, 200, 100)
                hover_color = (35, 180, 75)
                if button_rect.collidepoint(mouse_pos):
                    button_color = hover_color
                pygame.draw.rect(self.display, button_color, button_rect,border_radius=150)
                pygame.draw.rect(self.display, (100, 100, 100), button_rect, 5 ,border_radius=150)
                self.display.blit(text, text_rect)

            self.display.blit(back_text, back_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button, level, text, text_rect in self.buttons:
                            if button.collidepoint(mouse_pos):
                                game = Game(start_level=level)
                                game.run()
                        if back_button_rect.collidepoint(mouse_pos):
                            return
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Levels().run()