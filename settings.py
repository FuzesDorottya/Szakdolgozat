import pygame
import os

from scripts.utilities import image
from scripts.button import Button

class Settings:
    def __init__(self, main, screen, return_to="menu"):
        pygame.init()
        self.main = main
        self.screen = screen
        self.return_to = return_to
        self.screen_size = self.screen.get_size()
        width = 1920
        height = 1080
        self.display = pygame.Surface((width, height))
        self.scale = min(self.screen_size[0] / width, self.screen_size[1] / height)
        self.new_height = int(height * self.scale)
        self.new_width = int(width * self.scale)
        self.offset_x = (self.screen_size[0] - self.new_width) // 2
        self.offset_y = (self.screen_size[1] - self.new_height) // 2
        self.clock = pygame.time.Clock()

        self.game_volume = self.main.game_volume
        self.menu_volume = self.main.menu_volume
        
        self.back_save_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 45)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", width // 40)
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 30)
        self.buttons = []
        self.buttons_rect()
        self.settings_text = []
        self.setting_text()
    
    def buttons_rect(self):
        for i in range(4):
            gap = 300
            button_size = 100
            columns = 2
            grid_width = (columns * button_size) + ((columns - 1) * gap)
            start_x = (self.display.get_width() - grid_width) / 2
            start_y = 250
            column = i % columns
            row = i // columns
            button_x_position = start_x + column * (button_size + gap)
            button_y_position = start_y + row * (button_size + gap / 2)

            text = ""
            if (i+1) % 2 == 0:
                text = "+"
            else: text = "-"

            button = Button((button_x_position, button_y_position, button_size, button_size),
                            text,self.secondary_font, border_radius=40)
            self.buttons.append(button)
        back_button = Button((10, 20, 150, 80), "back",self.back_save_font, border_radius=150)
        self.buttons.append(back_button)
        save_button = Button((self.display.get_width() / 2 - 150/2, self.display.get_height() - 200, 150, 80), "save",self.back_save_font, border_radius=150)
        self.buttons.append(save_button)
    
    def setting_text(self):
        self.settings_text = []
        settings_texts = [f"menu music\n{round(self.menu_volume * 100)}%", f"game music\n{round(self.game_volume * 100)}%"]

        for i in range(len(settings_texts)):
            left_button = self.buttons[i * 2]
            right_button = self.buttons[i * 2 + 1]

            center_x = (left_button.rect.centerx + right_button.rect.centerx) / 2
            center_y = left_button.rect.centery

            split_text = settings_texts[i].split("\n")

            spacing = self.secondary_font.get_height()
            total_text_height = len(split_text) * spacing

            start_y = center_y - total_text_height / 2 + spacing / 2

            for j in range(len(split_text)):
                line = split_text[j]
                text_surface = self.secondary_font.render(line, True, (65, 65, 65))
                text_rect = text_surface.get_rect(center=(center_x, start_y + j * spacing))
                self.settings_text.append((text_surface, text_rect))

    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())
        settings_text = self.main_font.render("settings", True, (65, 65, 65))
        settings_text_rect = settings_text.get_rect(center=(self.display.get_width() / 2, 100))
       
        while True:
            self.display.blit(bgr, (0, 0))
            self.display.blit(settings_text, settings_text_rect)
            mouse_pos = pygame.mouse.get_pos()
            self.scales_mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)
            for button in self.buttons:
                button.draw(self.display, self.scales_mouse_pos)

            for text_surface, text_rect in self.settings_text:
                self.display.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(len(self.buttons)):
                            self.buttons[i].sound(event)
                            if self.buttons[i].rect.collidepoint(self.scales_mouse_pos):
                                if i == 0:
                                    self.menu_volume = max(0, self.menu_volume - 0.05)
                                elif i == 1:
                                    self.menu_volume = min(1.0, self.menu_volume + 0.05)
                                elif i == 2:
                                    self.game_volume = max(0, self.game_volume - 0.05)
                                elif i == 3:
                                    self.game_volume = min(1.0, self.game_volume + 0.05)
                                elif self.buttons[i].text == "back":
                                    return self.return_to
                                elif self.buttons[i].text == "save":
                                    self.main.change_volume("menu", self.menu_volume)
                                    self.main.change_volume("game", self.game_volume)
                                    return "save"
                                
                                self.setting_text()
            
            self.screen.fill((0,0,0))
            self.screen.blit(pygame.transform.scale(self.display, (self.new_width, self.new_height)), (self.offset_x, self.offset_y))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Settings().run()