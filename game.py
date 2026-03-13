import pygame
import os
import math

from scripts.utilities import image, images, Animation
from scripts.tilemap import Tilemap
from scripts.character_physics import Player, Ai
from scripts.clouds import Clouds
from scripts.button import Button

from scripts.pathfinding import Pathfinding

class Game:
    def __init__(self, screen, start_level = 0):
        pygame.init()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        width = 1920
        height = 1080
        self.pause_display = pygame.Surface((width, height))
        self.display = pygame.Surface((width//6, height//6))
        self.scale = min(self.screen_size[0] / width, self.screen_size[1] / height)
        self.new_height = int(height * self.scale)
        self.new_width = int(width * self.scale)
        self.offset_x = (self.screen_size[0] - self.new_width) // 2
        self.offset_y = (self.screen_size[1] - self.new_height) // 2
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]

        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 30)
        self.button_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", width // 40)
        
        self.paused = False
        self.buttons = []
        self.pause_buttons()
        self.pause_bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.pause_display.get_size())

        self.imgs = {
            "dirt": images("tiles/dirt"),
            "flowers": images("tiles/decor/flowers"),
            "large_decor": images("tiles/decor/large_decors"),
            "spikes": images("tiles/spikes"),
            "character_spawn": images("tiles/character_spawn"),
            "finish": images("tiles/finish"),
            "player/idle": Animation(images("characters/player/idle"), duration=6),
            "player/run": Animation(images("characters/player/run"), duration=5),
            "player/jump": Animation(images("characters/player/jump"), duration=10),
            "ai/idle": Animation(images("characters/ai/idle"), duration=6),
            "ai/run": Animation(images("characters/ai/run"), duration=5),
            "ai/jump": Animation(images("characters/ai/jump"), duration=10)
        }

        self.ambience = pygame.mixer.Sound("assets/sound_effects/ambience.wav")
        self.die = pygame.mixer.Sound("assets/sound_effects/die.wav")
        self.finish_sfx = pygame.mixer.Sound("assets/sound_effects/finish.wav")
        self.jump = pygame.mixer.Sound("assets/sound_effects/jump.wav")
        self.walk = pygame.mixer.Sound("assets/sound_effects/walk.wav")
        self.ambience.set_volume(0.15)
        self.die.set_volume(0.15)
        self.finish_sfx.set_volume(0.8)
        self.jump.set_volume(0.15)
        self.walk.set_volume(0.1)

        self.clouds_close = Clouds(image("clouds/0.png"), type = 0, count=4)
        self.clouds_far = Clouds(image("clouds/1.png"), type = 1, count=3)
        self.tilemap = Tilemap(self)
        self.player = Player(self, (0,0), (10, 11))
        self.pathfinding = Pathfinding(self.tilemap)
        self.ai = Ai(self, (0,0), (10, 11))

        self.level = start_level
        self.load_map(self.level)

        self.path = None
        self.ai_on = False
        self.last_node = None

    def load_map(self, map):
        self.tilemap.load(f"assets/maps/{map}.json")
        self.player.position = self.tilemap.get_player_spawn()
        self.player.air_time = 0

        self.offset = [0, 0]
        self.dead = False
        self.finish = False

        self.transition_step = 50
        self.transition = True
        self.transition_newmap = True
    
    def pause_buttons(self):
        button_names = ["resume", "settings", "controls", "return to main menu"]
        center_y = self.pause_display.get_height() / 2 - 75
        y_offset = 150

        for i in range(len(button_names)):
            name = button_names[i]
            button_rect = pygame.Rect(0, 0, 550, 100)
            button_rect.centerx = self.pause_display.get_width() / 2
            button_rect.centery = center_y + i * y_offset

            button = Button(button_rect, name, self.button_font, border_radius=150)
            self.buttons.append(button)

    def pause(self):
        self.ambience.stop()
        self.die.stop()
        self.finish_sfx.stop()
        self.jump.stop()
        self.walk.stop()

        pause_text = self.main_font.render("paused", True, (65,65,65))
        pause_text_rect = pause_text.get_rect(center=(self.pause_display.get_width() / 2, 100))
        self.pause_display.blit(self.pause_bgr, (0,0))
        self.pause_display.blit(pause_text, pause_text_rect) 

        for button in self.buttons:
            button.draw(self.pause_display, self.scaled_mouse_pos)

        self.screen.fill((0,0,0))
        self.screen.blit(pygame.transform.scale(self.pause_display, (self.new_width, self.new_height)), (self.offset_x, self.offset_y))
    
    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.scaled_mouse_pos = ((mouse_pos[0] - self.offset_x) / self.scale, (mouse_pos[1] - self.offset_y) / self.scale)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        self.movement[0] = False
                        self.movement[1] = False 
                        self.paused = not self.paused
                    if event.key == pygame.K_h:
                        self.ai_on = True

                        start = self.last_node
                        goal = self.pathfinding.finish_node()

                        self.ai.position = [start[0] * self.tilemap.tile_size, (start[1] + 1) * self.tilemap.tile_size - self.ai.character_size[1]]
                        self.ai.velocity = [0,0]
                        self.ai.collisions["down"] = True
                        self.ai.air_time = 0
                        self.ai.jump_target = None
                        self.ai.path_index = 0
                                            
                        if start and goal:
                            self.path = self.pathfinding.astar_pathfinding(start,goal)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                if self.paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in self.buttons:
                                button.sound(event)
                                if button.rect.collidepoint(self.scaled_mouse_pos):
                                    if button.text == "resume":
                                        self.paused = False
                                    if button.text == "return to main menu":
                                        return "menu"
                                    if button.text == "settings":
                                        return "settings_game"
                                    if button.text == "controls":
                                        return "controls_game"

            if not self.paused:
                if self.ambience.get_num_channels() == 0:
                    self.ambience.play(-1)
                if self.finish:
                    if self.level < len(os.listdir("assets/maps")) - 1:
                        self.level += 1
                        self.load_map(self.level)
                    else:
                        return "levels"
                
                if self.transition:
                    if self.transition_newmap:
                        self.transition_step -= 1
                        if self.transition_step <= 0:
                            self.transition_step = 0
                            self.transition = False
                    else:
                        self.transition_step += 1
                        if self.transition_step >= 50:
                            self.transition_step = 50
                            self.transition = False
                    
                if self.dead:
                    self.load_map(self.level)
            
                character_rect = pygame.Rect(self.player.position[0], 
                                            self.player.position[1], 
                                            self.player.character_size[0], 
                                            self.player.character_size[1])
                self.offset[0] += (character_rect.centerx - self.display.get_width() / 2 - self.offset[0]) / 6
                self.offset[1] += (character_rect.centery - self.display.get_height() / 2 - self.offset[1]) / 6

                for spike in self.tilemap.neighbouring_spikes(self.player.position):
                    if character_rect.colliderect(spike["rect"]):
                        offset = (spike["rect"].x - self.player.position[0],
                                    spike["rect"].y - self.player.position[1])

                        if self.player.mask.overlap(spike["mask"], offset):
                            self.dead = True
                            self.die.play()
                            break

                self.clouds_far.update()
                self.clouds_close.update()
            
                if not self.dead:
                    self.player.update(self.tilemap, 
                                    (self.movement[1] - self.movement[0], 0))

                current_node = self.pathfinding.player_current_node(character_rect)
                if current_node:
                        self.last_node = current_node
                
                ai_rect = pygame.Rect(self.ai.position[0], 
                                                self.ai.position[1], 
                                                self.ai.character_size[0], 
                                                self.ai.character_size[1])
                for rect in self.tilemap.finish_tile():
                    if ai_rect.colliderect(rect):
                        self.ai_on = False
                if self.ai_on and self.path:
                    self.ai.update(self.tilemap)
                    
            self.display.blit(bgr, (0, 0))
            render_offset = (int(self.offset[0]), int(self.offset[1]))

            self.clouds_far.render(self.display, render_offset)
            self.clouds_close.render(self.display, render_offset)
            self.tilemap.render(self.display, render_offset)
            
            if self.ai_on and self.path:
                self.ai.render(self.display, render_offset)
            if not self.dead:
                self.player.render(self.display, render_offset)
            
            if self.transition_step:
                center_x = self.display.get_width() // 2
                center_y = self.display.get_height() // 2
                c_radius = math.sqrt(center_x**2 + center_y**2)

                transition_surface = pygame.Surface(self.display.get_size())
                transition_surface.fill((10, 10, 50))
                pygame.draw.circle(transition_surface, (0, 0, 0), 
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   ((50 - abs(self.transition_step)) / 50) * c_radius)
                transition_surface.set_colorkey((0, 0, 0))
                self.display.blit(transition_surface, (0, 0))
            
            self.screen.fill((0,0,0))
            self.screen.blit(pygame.transform.scale(self.display, (self.new_width, self.new_height)), (self.offset_x, self.offset_y))

            if self.paused:
                self.pause()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()