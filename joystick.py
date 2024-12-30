import pygame

import image


def updates(x, y, pos):
    xabs = pos[0] - x
    yabs = pos[1] - y
    posabs = (xabs, yabs)
    return posabs


class JoyStick:
    def __init__(self, surface, x, y):
        self.surface: pygame.Surface = surface
        self.back = image.raw['joy.back']
        self.forge = image.raw['joy.forge']
        self.pos = (x, y)
        self.x, self.y = 0, 0

    def move(self, pos):
        self.pos = pos

    def update(self, x, y):
        self.x, self.y = x, y
        self.surface.blit(self.back, (x - 150 // 2, y - 150 // 2))
        self.surface.blit(self.forge, (self.pos[0] - 25, self.pos[1] - 25))

    def upd(self, x, y):
        self.x, self.y = x, y
        return updates(x, y, self.pos)
