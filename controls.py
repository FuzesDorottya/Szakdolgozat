import pygame

from scripts.utilities import image
from scripts.button import Button

class Controls:
    def __init__(self, screen, return_to = "menu"):
        pygame.init()
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

        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 30)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", width // 40)
        self.back_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 45)
        self.buttons = []
        self.buttons_rect()
        self.control_texts = []
        self.controls_text()
    
    def buttons_rect(self):
        back_button = Button((10, 20, 150, 80), "back",self.back_font, border_radius=150)
        self.buttons.append(back_button)

    def controls_text(self):
        control_text = ["Go left : A", "Go right : D", "Jump : W", "Pause : ESCAPE", "Help: H"]
        y_offset = 150

        for i in range(len(control_text)):
            text_surface = self.secondary_font.render(control_text[i], True, (65, 65, 65))
            text_rect = text_surface.get_rect(center=(self.display.get_width() / 2, 300 + i * y_offset))
            self.control_texts.append((text_surface, text_rect))
    
    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())

        controls_text = self.main_font.render("Controls", True, (65, 65, 65))
        controls_text_rect = controls_text.get_rect(center=(self.display.get_width() / 2, 100))
       
        while True:
            self.display.blit(bgr, (0, 0))
            self.display.blit(controls_text, controls_text_rect)
            mouse_pos = pygame.mouse.get_pos()
            self.scales_mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)
            for button in self.buttons:
                button.draw(self.display, self.scales_mouse_pos)

            for text_surface, text_rect in self.control_texts:
                self.display.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            button.sound(event)
                            if button.rect.collidepoint(self.scales_mouse_pos):
                                return self.return_to
            
            self.screen.fill((0,0,0))
            self.screen.blit(pygame.transform.scale(self.display, (self.new_width, self.new_height)), (self.offset_x, self.offset_y))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Controls().run()