######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import threading
from random import seed

import pygame.freetype

from contact import *
import time
from base import *

pygame.freetype.init()
import font
import image
import random

image.init()


class Pos:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x += x
        self.y += y


class Map(list):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

    def fresh1(self, surface, center, pos, num):
        self.x = int(-pos.x // blocksize)
        self.y = int(-pos.y // blocksize)
        for i in range(-renderdistance // blocksize, renderdistance // blocksize + 2):
            for j in range(-renderdistance // blocksize, renderdistance // blocksize + 2):
                flg = 0
                for k in self:
                    if k.x == i + self.x and k.y == j + self.y:
                        flg = 1
                if not flg:
                    blo = Block(surface, i + self.x, j + self.y, center, pos.x, pos.y)
                    blo.init(pos.x, pos.y)
                    self.append(blo)
        num.num = 0

    def fresh(self, surface, center, pos, num):
        num.num = 1

        threading.Thread(target=self.fresh1, args=(surface, center, pos, num)).start()


class Block:
    def __init__(self, surface, x, y, center, x1=0, y1=0):
        self.surface = surface
        self.x = x
        self.y = y
        self.x1 = x * blocksize + center[0] // 2 + x1
        self.y1 = y * blocksize + center[1] // 2 + y1
        self.center = center
        self.seed = hash((x, y)) + (contact.seed if contact.seed != 'random' else time.time())
        self.images = []

    def init(self, x=0, y=0):
        x = self.center[0] // 2 + x
        y = self.center[1] // 2 + y
        random.seed(self.seed)
        for i in range((blocksize * 2) ** 2 // 100000):
            i = Image(self.surface,
                      randint(-blocksize // 2 + self.x * blocksize, blocksize // 2 + self.x * blocksize) + x,
                      randint(-blocksize // 2 + self.y * blocksize, blocksize // 2 + self.y * blocksize) + y,
                      image=image.raw['grass'])
            self.images.append(i)
            for i in range(3):
                i = Image(self.surface,
                          randint(-blocksize // 2 + self.x * blocksize, blocksize // 2 + self.x * blocksize) + x,
                          randint(-blocksize // 2 + self.y * blocksize, blocksize // 2 + self.y * blocksize) + y,
                          image=image.raw['flown'])
                self.images.append(i)
        for i in range((blocksize * 2) ** 2 // 1000000):
            i = Image(self.surface,
                      randint(-blocksize // 2 + self.x * blocksize, blocksize // 2 + self.x * blocksize) + x,
                      randint(-blocksize // 2 + self.y * blocksize, blocksize // 2 + self.y * blocksize) + y,
                      image=image.raw['flower1'])
            self.images.append(i)
            i = Image(self.surface,
                      randint(-blocksize // 2 + self.x * blocksize, blocksize // 2 + self.x * blocksize) + x,
                      randint(-blocksize // 2 + self.y * blocksize, blocksize // 2 + self.y * blocksize) + y,
                      image=image.raw['flower2'])
            self.images.append(i)
        random.seed(contact.seed if contact.seed != 'random' else time.time())

    def distance(self, x, y):
        x1 = self.x1 - x
        x2 = self.y1 - y
        return (x1 ** 2 + x2 ** 2) ** 0.5

    def update(self, x, y, scale, center, maps, pos):
        self.x1 += x
        self.y1 += y
        self.center = center
        if self.distance(*self.center) < renderdistance:
            x1, y1 = self.center[0] // 2, self.center[1] // 2
            for i in self.images:
                i.update(x, y, scale, center, (x1, y1))
        else:
            for i in self.images:
                i.x += x
                i.y += y
            if self.distance(*self.center) > renderdistance + 2000:
                maps.remove(self)
