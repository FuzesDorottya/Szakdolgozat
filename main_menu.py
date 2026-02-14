import sys
import pygame

from scripts.utilities import image
from levels import Levels

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.clock = pygame.time.Clock()
        
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.buttons = []
        self.buttons_rect()
    
    def buttons_rect(self):
        button_names = ["levels", "options", "controls", "quit"]
        center_y = self.display.get_height() / 2 - 75
        y_offset = 150

        for i in range(len(button_names)):
            name = button_names[i]
            button_rect = pygame.Rect(0, 0, 450, 100)
            button_rect.centerx = self.display.get_width() / 2
            button_rect.centery = center_y + i * y_offset

            text = self.main_font.render(name, True, (65, 65, 65)) 
            text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - 8))

            self.buttons.append((name, button_rect, text, text_rect))
    
    def run(self):
        self.running = True
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())
        
        while self.running:
            self.display.blit(bgr, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for name, button_rect, text, text_rect in self.buttons:
                button_color = (55, 200, 100)
                hover_color = (35, 180, 75)
                if button_rect.collidepoint(mouse_pos):
                    button_color = hover_color
                pygame.draw.rect(self.display, button_color, button_rect,border_radius=150)
                pygame.draw.rect(self.display, (100, 100, 100), button_rect, 5 ,border_radius=150)
                self.display.blit(text, text_rect)
           
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for name, button_rect, text, text_rect in self.buttons:
                            if button_rect.collidepoint(mouse_pos):
                                if name == "levels":
                                    Levels().run()
                                if name == "quit":
                                    pygame.quit()
                                    sys.exit()
                    
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Menu().run()