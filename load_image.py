import os
import pygame

def load_image(name):
    return pygame.image.load(os.path.join('res', 'img', name))

