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
        self.combined_surface = None  # 新增属性，用于存储合并后的 Surface

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
        self.create_combined_surface()  # 初始化时创建合并后的 Surface

    def create_combined_surface(self):
        # 计算合并后的 Surface 的大小
        min_x = min([img.x for img in self.images])
        min_y = min([img.y for img in self.images])
        max_x = max([img.x + img.image.get_width() for img in self.images])
        max_y = max([img.y + img.image.get_height() for img in self.images])
        width = max_x - min_x
        height = max_y - min_y

        # 创建合并后的 Surface
        self.combined_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for img in self.images:
            offset_x = img.x - min_x
            offset_y = img.y - min_y
            self.combined_surface.blit(img.image, (offset_x, offset_y))

    def distance(self, x, y):
        x1 = self.x1 - x
        x2 = self.y1 - y
        return (x1 ** 2 + x2 ** 2) ** 0.5

    def update(self, x, y, scale, center, maps, pos):
        self.x1 += x
        self.y1 += y
        self.center = center
        if self.distance(*self.center) < renderdistance:
            # 缩放合并后的 Surface
            scaled_surface = pygame.transform.scale(self.combined_surface,
                                                    (int(self.combined_surface.get_width() * scale),
                                                     int(self.combined_surface.get_height() * scale)))
            # 计算缩放后的 Surface 的中心点偏移量
            offset_x = scaled_surface.get_width() // 2
            offset_y = scaled_surface.get_height() // 2
            # 计算绘制位置，以 center 为中心点
            draw_x = (self.x1 - center[0]) * scale + center[0] - offset_x
            draw_y = (self.y1 - center[1]) * scale + center[1] - offset_y
            # 绘制缩放后的 Surface
            self.surface.blit(scaled_surface, (draw_x, draw_y))

        else:
            for i in self.images:
                i.x += x
                i.y += y
            if self.distance(*self.center) > renderdistance + 2000:
                maps.remove(self)
