import os
import pygame

images_path = 'assets/images/'

def image(path):
    img = pygame.image.load(images_path + path).convert()
    return img

def images(path):
    imgs = []
    for img in sorted(os.listdir(images_path + path)):
        imgs.append(image(path + '/' + img))
    return imgs