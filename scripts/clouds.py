import random
import pygame

class Cloud:
    def __init__(self, position, image, speed):
        self.position = list(position)
        self.image = image 
        self.image.set_alpha(100)
        self.speed = speed

    def update(self):
        self.position[0] -= self.speed

    def render(self, surface, offset=(0, 0)):
        render_position = (self.position[0] - offset[0], 
                           self.position[1] - offset[1])

        wrap_range_width = surface.get_width() + self.image.get_width()
        wrap_range_height = surface.get_height() + self.image.get_height()
        
        surface.blit(self.image,
                     (render_position[0] % wrap_range_width - self.image.get_width(),
                      render_position[1] % wrap_range_height - self.image.get_height()))


class Clouds: 
    def __init__(self, image, count):
        self.clouds = []
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        for cloud in range(count):
            cloud_scale = random.uniform(0.5, 1.5)
            speed = 0.05 / cloud_scale
            cloud_size = pygame.transform.scale(image, 
                                                (int(image.get_width() * cloud_scale),
                                                 int(image.get_height() * cloud_scale)))
            
            self.clouds.append(Cloud((random.uniform(0, screen_width), random.uniform(0, screen_height)),
                                     cloud_size,
                                     speed))

    def update(self):
        for cloud in self.clouds:
            cloud.update()
    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
