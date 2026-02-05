import os
import pygame

def image(path):
    img = pygame.image.load("assets/images/" + path).convert()
    return img

def images(path):
    imgs = []
    for img in sorted(os.listdir("assets/images/" + path)):
        imgs.append(image(path + "/" + img))
    return imgs