######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import pygame
from pygame import Surface

import font
import image
import item_info
from base import Numbers
from item_info import rawall

pygame.init()
image.init()
# todo 这里用来搞物品
weapon = None

weapondict = {}
for i in rawall['weapon_type']:
    weapondict[i] = image.raw['item.' + i]
items = ['normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'normal']
lvl = [1, 1, 1, 1, 1, 1, 1]
bonus = [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
         [None, None]]
bonuslvl = [[1, 1], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
itemdict = {}
for i in rawall['item_type']:
    itemdict[i] = image.raw['item.' + i]


class Bag:
    def __init__(self, surface, sizex, sizey):
        self.point = image.raw['point']
        self.surface: pygame.Surface = surface
        self.sizex = sizex
        self.sizey = sizey
        self.tick = 0
        self.bag = list([[None for __ in range(5)] for _ in range(5)])
        self.lvl = list([[None for __ in range(5)] for _ in range(5)])
        self.blocks = list([[None for __ in range(5)] for _ in range(5)])
        self.itemblocks = list([None for __ in range(9)])
        self.bonus = list([[[None, None] for __ in range(5)] for _ in range(5)])
        self.bonuslvl = list([[[None, None] for __ in range(5)] for _ in range(5)])
        self.select = None
        self.selectlvl = None
        self.selectbonus = [None, None]
        self.selectbonuslvl = [None, None]

        self.craft_bag = list([[None for __ in range(3)] for _ in range(3)])
        self.craft_lvl = list([[None for __ in range(3)] for _ in range(3)])
        self.craft_blocks = list([[None for __ in range(3)] for _ in range(3)])
        self.craft_bonus = list([[[None, None] for __ in range(3)] for _ in range(3)])
        self.craft_bonuslvl = list([[[None, None] for __ in range(3)] for _ in range(3)])

        self.craft_result_bag = None
        self.craft_result_lvl = None
        self.craft_result_blocks = None
        self.craft_result_bonus = [None, None]
        self.craft_result_bonuslvl = [None, None]


        self.additem('lightning', 6, ['healthPoint', 'healthPoint'], [10, 10])
        self.additem('lightning', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('lightning', 6)
        self.additem('lightning', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('lightning', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('wide', 6)
        self.additem('wide', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('phosphor', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('puncture', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('lightning', 6)
        self.additem('puncture', 6)
        self.additem('normal', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('normal', 6, ['healthPoint', 'healthPoint'], [1, 1])
        self.additem('wide', 6)
        self.additem('healthPoint', 6)
        self.additem('normal', 1)
        self.additem('normal', 1)

    def additem(self, types, lvls, bonuses=None, bonuslvls=None):
        if bonuses is None:
            bonuses = [None, None]
        if bonuslvls is None:
            bonuslvls = [None, None]
        for indexi, item1 in enumerate(self.bag):
            for indexj, item2 in enumerate(item1):
                if item2 is None:
                    self.bag[indexi][indexj] = types
                    self.lvl[indexi][indexj] = lvls
                    self.bonus[indexi][indexj] = bonuses
                    self.bonuslvl[indexi][indexj] = bonuslvls
                    return

    def update(self, ind, tick, player, elst, plst, indx):

        ind %= len(items)
        x = font.normal.render('Weapon(武器): ' + str(weapon), 1, 'black')
        self.surface.blit(x, (self.sizex + 2, self.sizey - 153))
        x = font.normal.render('Weapon(武器): ' + str(weapon), 1, 'white')
        self.surface.blit(x, (self.sizex, self.sizey - 155))
        pygame.draw.rect(self.surface, 'black', ((self.sizex - 8, self.sizey - 118), (70, 70)), 3, 10)
        pygame.draw.rect(self.surface, 'white', ((self.sizex - 10, self.sizey - 120), (70, 70)), 3, 10)
        if weapon is not None:
            self.surface.blit(weapondict[weapon], (self.sizex, self.sizey - 110))

        x = font.normal.render('Items(物品栏): ' + str(lvl[ind]) + ' ' + str(items[ind]), 1, 'black')
        self.surface.blit(x, (self.sizex + 2, self.sizey - 43))
        x = font.normal.render('Items(物品栏): ' + str(lvl[ind]) + ' ' + str(items[ind]), 1, 'white')
        self.surface.blit(x, (self.sizex, self.sizey - 45))
        pygame.draw.rect(self.surface, 'black', ((self.sizex - 8, self.sizey - 8), (60 * len(items) + 10, 70)), 3, 10)
        pygame.draw.rect(self.surface, 'white', ((self.sizex - 10, self.sizey - 10), (60 * len(items) + 10, 70)), 3, 10)
        flag = 0
        scale = 1
        if items[ind] is not None:
            timesleep = eval(item_info.raw[items[ind]]['timesleep'])
            for i in bonus[ind]:
                if i is None: continue
                timesleep -= eval(item_info.bonusInfo[i]['timesleep'])
                if timesleep == 0: timesleep = 0

            if tick - self.tick > timesleep and player.type == 1 and len(elst) > 0:
                self.tick = tick
                if type(indx) == Numbers and items[ind] is not None:
                    player.summon_pond(plst, elst, typ=items[indx.num % items.__len__()],
                                       lvl=lvl[indx.num % lvl.__len__()], bonus=bonus[indx.num % items.__len__()],
                                       bonuslvl=bonuslvl[indx.num % items.__len__()])
                    indx.num += 1
            scale = (tick - self.tick) / (timesleep + 0.001)
        else:
            if player.type == 1:
                indx.num += 1

        for index, item in enumerate(items):
            if ind == index: pygame.draw.rect(self.surface, 'black',
                                              ((self.sizex + index * 60 - 3, self.sizey - 3), (60, 60)), 3, 10)
            if ind == index:
                pygame.draw.rect(self.surface, 'white', ((self.sizex + index * 60 - 5, self.sizey - 5), (60, 60)), 3,
                                 10)
                pygame.draw.rect(self.surface, 'white',
                                 (((self.sizex + index * 60 - 5), self.sizey - 5 + 60 * scale), (60, 60 * (1 - scale))))
            x = font.small.render(str(lvl[index]), True, (0, 0, 0))
            x2 = font.small.render(str(lvl[index]), True, (255, 255, 255))
            if item is not None:
                self.surface.blit(itemdict[item], (self.sizex + index * 60, self.sizey))
                self.surface.blit(x, (self.sizex + index * 60 + 2, self.sizey + 2))
                self.surface.blit(x2, (self.sizex + index * 60, self.sizey))
                for indexx, ix in enumerate(bonus[index]):
                    if ix is not None:
                        x1 = itemdict[ix]
                        x1 = pygame.transform.scale(x1, (20, 20))
                        x = font.small.render(str(bonuslvl[index][indexx]), True, (0, 0, 0))
                        x2 = font.small.render(str(bonuslvl[index][indexx]), True, (255, 255, 255))
                        self.surface.blit(x1, (self.sizex + 25 + index * 60, self.sizey + indexx * 20))
                        self.surface.blit(x, (self.sizex + 25 + 2 + index * 60, self.sizey + indexx * 20 + 2))
                        self.surface.blit(x2, (self.sizex + 25 + index * 60, self.sizey + indexx * 20))

    def moving(self, pos):
        if self.select is not None:
            self.surface.blit(itemdict[self.select], (pos[0] - 25, pos[1] - 25))
            x = font.small.render(str(self.selectlvl), True, (0, 0, 0))
            x2 = font.small.render(str(self.selectlvl), True, (255, 255, 255))
            self.surface.blit(x, (pos[0] - 25 + 2, pos[1] - 25 + 2))
            self.surface.blit(x2, (pos[0] - 25, pos[1] - 25))
            for indexx, ix in enumerate(self.selectbonus):
                print(ix)
                if ix is not None:
                    x1 = itemdict[ix]
                    x1 = pygame.transform.scale(x1, (20, 20))
                    x = font.small.render(str(self.selectbonuslvl[indexx]), True, (0, 0, 0))
                    x2 = font.small.render(str(self.selectbonuslvl[indexx]), True, (255, 255, 255))
                    self.surface.blit(x1, (pos[0] - 25 + 25, pos[1] - 25 + indexx * 20))
                    self.surface.blit(x, (pos[0] - 25 + 25 + 2, pos[1] - 25 + indexx * 20 + 2))
                    self.surface.blit(x2, (pos[0] - 25 + 25, pos[1] - 25 + indexx * 20))

    def background(self, center):
        surf = Surface((center[0] * 2, center[1] * 2))
        surf.fill('black')
        surf.set_alpha(80)
        self.surface.blit(surf, (0, 0))
        weight = center[0] * 2 - 200
        height = center[1] * 2 - 200
        minim = min(weight, height)

        f = font.chin.size('MY BAG 我的背包')[0]
        x = font.chin.render('MY BAG 我的背包', True, (255, 0, 255))
        x3 = font.chin.render('MY BAG 我的背包', True, (255, 255, 0))
        x2 = font.chin.render('MY BAG 我的背包', True, (255, 255, 255))
        self.surface.blit(x, (center[0] + 4 - f // 2, 50 + 4))
        self.surface.blit(x3, (center[0] + 2 - f // 2, 50 + 2))
        self.surface.blit(x2, (center[0] - f // 2, 50))
        pygame.draw.rect(self.surface, "#C26C22", ((100, 100), (weight, height)), border_radius=30)
        for indexi, item1 in enumerate(self.bag):
            for indexj, item2 in enumerate(item1):
                if item2 is None:
                    pass
                else:
                    x = font.small.render(str(self.lvl[indexi][indexj]), True, (0, 0, 0))
                    x2 = font.small.render(str(self.lvl[indexi][indexj]), True, (255, 255, 255))
                    item = pygame.transform.scale(itemdict[item2], ((minim // 7 - 5), (minim // 7 - 5)))
                    self.surface.blit(item, (minim // 7 * indexi + 120, minim // 7 * indexj + 120))
                    self.surface.blit(x, (minim // 7 * indexi + 120 + 10, minim // 7 * indexj + 120 + 10))
                    self.surface.blit(x2, (minim // 7 * indexi + 120 + 8, minim // 7 * indexj + 120 + 8))

                    for indexx, ix in enumerate(self.bonus[indexi][indexj]):
                        if ix is not None:
                            x1 = itemdict[ix]
                            x1 = pygame.transform.scale(x1, ((minim // 7 - 5) / 5 * 2, (minim // 7 - 5) / 5 * 2))
                            x = font.small.render(str(self.bonuslvl[indexi][indexj][indexx]), True, (0, 0, 0))
                            x2 = font.small.render(str(self.bonuslvl[indexi][indexj][indexx]), True, (255, 255, 255))
                            self.surface.blit(x1, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5,
                                                   minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))
                            self.surface.blit(x, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + 2,
                                                  minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2 + 2))
                            self.surface.blit(x2, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5,
                                                   minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))

                pygame.draw.rect(self.surface, 'black', (
                    (minim // 7 * indexi + 120 + 2, minim // 7 * indexj + 120 + 2), (minim // 7 - 5, minim // 7 - 5)),
                                 3,
                                 10)
                x = pygame.draw.rect(self.surface, 'white', (
                    (minim // 7 * indexi + 120, minim // 7 * indexj + 120), (minim // 7 - 5, minim // 7 - 5)), 3, 10)
                self.blocks[indexi][indexj] = x

        for indexi, item2 in enumerate(items):
            if item2 is None:
                pass
            else:
                x = font.small.render(str(lvl[indexi]), True, (0, 0, 0))
                x2 = font.small.render(str(lvl[indexi]), True, (255, 255, 255))
                item = pygame.transform.scale(itemdict[item2], ((minim // 7 - 5), (minim // 7 - 5)))
                self.surface.blit(item, (minim // 7 * indexi + 120, minim // 7 * 5 + 140))
                self.surface.blit(x, (minim // 7 * indexi + 120 + 10, minim // 7 * 5 + 140 + 10))
                self.surface.blit(x2, (minim // 7 * indexi + 120 + 8, minim // 7 * 5 + 140 + 8))
                for indexx, ix in enumerate(bonus[indexi]):
                    if ix is not None:
                        x1 = itemdict[ix]
                        x1 = pygame.transform.scale(x1, ((minim // 7 - 5) / 5 * 2, (minim // 7 - 5) / 5 * 2))
                        x = font.small.render(str(bonuslvl[indexi][indexx]), True, (0, 0, 0))
                        x2 = font.small.render(str(bonuslvl[indexi][indexx]), True, (255, 255, 255))
                        self.surface.blit(x1, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5,
                                               minim // 7 * 5 + 140 + indexx * (minim // 7 - 5) / 5 * 2))
                        self.surface.blit(x, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + 2,
                                              minim // 7 * 5 + 140 + indexx * (minim // 7 - 5) / 5 * 2 + 2))
                        self.surface.blit(x2, (minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5,
                                               minim // 7 * 5 + 140 + indexx * (minim // 7 - 5) / 5 * 2))
            pygame.draw.rect(self.surface, 'black', (
                (minim // 7 * indexi + 120 + 2, minim // 7 * 5 + 140 + 2), (minim // 7 - 5, minim // 7 - 5)), 3, 10)
            x = pygame.draw.rect(self.surface, 'white', (
                (minim // 7 * indexi + 120, minim // 7 * 5 + 140), (minim // 7 - 5, minim // 7 - 5)), 3, 10)
            self.itemblocks[indexi] = x

        for indexi, item1 in enumerate(self.craft_bag):
            for indexj, item2 in enumerate(item1):
                if item2 is None:
                    pass
                else:
                    x = font.small.render(str(self.craft_lvl[indexi][indexj]), True, (0, 0, 0))
                    x2 = font.small.render(str(self.craft_lvl[indexi][indexj]), True, (255, 255, 255))
                    item = pygame.transform.scale(itemdict[item2], ((minim // 7 - 5), (minim // 7 - 5)))
                    self.surface.blit(item, (minim // 7 * indexi + 120 + minim // 7 * 6, minim // 7 * indexj + 120))
                    self.surface.blit(x,
                                      (minim // 7 * indexi + 120 + 10 + minim // 7 * 6, minim // 7 * indexj + 120 + 10))
                    self.surface.blit(x2,
                                      (minim // 7 * indexi + 120 + 8 + minim // 7 * 6, minim // 7 * indexj + 120 + 8))

                    for indexx, ix in enumerate(self.craft_bonus[indexi][indexj]):
                        if ix is not None:
                            x1 = itemdict[ix]
                            x1 = pygame.transform.scale(x1, ((minim // 7 - 5) / 5 * 2, (minim // 7 - 5) / 5 * 2))
                            x = font.small.render(str(self.craft_bonuslvl[indexi][indexj][indexx]), True, (0, 0, 0))
                            x2 = font.small.render(str(self.craft_bonuslvl[indexi][indexj][indexx]), True,
                                                   (255, 255, 255))
                            self.surface.blit(x1, (
                            minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + minim // 7 * 6,
                            minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))
                            self.surface.blit(x, (
                            minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + 2 + minim // 7 * 6,
                            minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2 + 2))
                            self.surface.blit(x2, (
                            minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + minim // 7 * 6,
                            minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))

                pygame.draw.rect(self.surface, 'black', (
                    (minim // 7 * indexi + 120 + 2 + minim // 7 * 6, minim // 7 * indexj + 120 + 2),
                    (minim // 7 - 5, minim // 7 - 5)),
                                 3,
                                 10)
                x = pygame.draw.rect(self.surface, 'white', (
                    (minim // 7 * indexi + 120 + minim // 7 * 6, minim // 7 * indexj + 120),
                    (minim // 7 - 5, minim // 7 - 5)), 3, 10)
                self.craft_blocks[indexi][indexj] = x

        indexi = 3;
        indexj = 1
        point = pygame.transform.scale(self.point, ((minim // 7 - 5), (minim // 7 - 5)))
        self.surface.blit(point, (minim // 7 * indexi + 120 + minim // 7 * 6, minim // 7 * indexj + 120))

        item2 = self.craft_result_bag
        indexi = 4;
        indexj = 1
        if item2 is None:
            pass
        else:
            x = font.small.render(str(self.craft_result_lvl), True, (0, 0, 0))
            x2 = font.small.render(str(self.craft_result_lvl), True, (255, 255, 255))
            item = pygame.transform.scale(itemdict[item2], ((minim // 7 - 5), (minim // 7 - 5)))
            self.surface.blit(item, (minim // 7 * indexi + 120 + minim // 7 * 6, minim // 7 * indexj + 120))
            self.surface.blit(x,
                              (minim // 7 * indexi + 120 + 10 + minim // 7 * 6, minim // 7 * indexj + 120 + 10))
            self.surface.blit(x2,
                              (minim // 7 * indexi + 120 + 8 + minim // 7 * 6, minim // 7 * indexj + 120 + 8))

            for indexx, ix in enumerate(self.craft_result_bonus):
                if ix is not None:
                    x1 = itemdict[ix]
                    x1 = pygame.transform.scale(x1, ((minim // 7 - 5) / 5 * 2, (minim // 7 - 5) / 5 * 2))
                    x = font.small.render(str(self.craft_result_bonuslvl[indexx]), True, (0, 0, 0))
                    x2 = font.small.render(str(self.craft_result_bonuslvl[indexx]), True,
                                           (255, 255, 255))
                    self.surface.blit(x1, (
                        minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + minim // 7 * 6,
                        minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))
                    self.surface.blit(x, (
                        minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + 2 + minim // 7 * 6,
                        minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2 + 2))
                    self.surface.blit(x2, (
                        minim // 7 * indexi + 120 + (minim // 7 - 5) / 5 * 2 + 5 + minim // 7 * 6,
                        minim // 7 * indexj + 120 + indexx * (minim // 7 - 5) / 5 * 2))

        pygame.draw.rect(self.surface, 'black', (
            (minim // 7 * indexi + 120 + 2 + minim // 7 * 6, minim // 7 * indexj + 120 + 2),
            (minim // 7 - 5, minim // 7 - 5)),
                         3,
                         10)
        x = pygame.draw.rect(self.surface, 'white', (
            (minim // 7 * indexi + 120 + minim // 7 * 6, minim // 7 * indexj + 120),
            (minim // 7 - 5, minim // 7 - 5)), 3, 10)
        self.craft_result_blocks = x

    def click(self, event: pygame.event.Event):

        pos = event.pos
        if event.button == 1:
            print(pos)
            for indexi, item1 in enumerate(self.blocks):
                for indexj, item2 in enumerate(item1):
                    if type(item2) == pygame.rect.Rect:
                        if item2.collidepoint(pos):
                            sele = self.select
                            sele2 = self.selectlvl
                            sele3 = self.selectbonus
                            sele4 = self.selectbonuslvl
                            self.select = self.bag[indexi][indexj]
                            self.selectlvl = self.lvl[indexi][indexj]
                            self.selectbonus = self.bonus[indexi][indexj]
                            self.selectbonuslvl = self.bonuslvl[indexi][indexj]
                            self.bag[indexi][indexj] = sele
                            self.lvl[indexi][indexj] = sele2
                            self.bonus[indexi][indexj] = sele3
                            self.bonuslvl[indexi][indexj] = sele4
            for indexi, item2 in enumerate(self.itemblocks):
                if type(item2) == pygame.rect.Rect:
                    if item2.collidepoint(pos) and self.select not in rawall['bonus_type']:
                        sele = self.select
                        sele2 = self.selectlvl
                        sele3 = self.selectbonus
                        sele4 = self.selectbonuslvl
                        self.select = items[indexi]
                        self.selectlvl = lvl[indexi]
                        self.selectbonus = bonus[indexi]
                        self.selectbonuslvl = bonuslvl[indexi]
                        items[indexi] = sele
                        lvl[indexi] = sele2
                        bonus[indexi] = sele3
                        bonuslvl[indexi] = sele4
            for indexi, item1 in enumerate(self.craft_blocks):
                for indexj, item2 in enumerate(item1):
                    if type(item2) == pygame.rect.Rect:
                        if item2.collidepoint(pos):
                            sele = self.select
                            sele2 = self.selectlvl
                            sele3 = self.selectbonus
                            sele4 = self.selectbonuslvl
                            self.select = self.craft_bag[indexi][indexj]
                            self.selectlvl = self.craft_lvl[indexi][indexj]
                            self.selectbonus = self.craft_bonus[indexi][indexj]
                            self.selectbonuslvl = self.craft_bonuslvl[indexi][indexj]
                            self.craft_bag[indexi][indexj] = sele
                            self.craft_lvl[indexi][indexj] = sele2
                            self.craft_bonus[indexi][indexj] = sele3
                            self.craft_bonuslvl[indexi][indexj] = sele4
            item2 = self.craft_result_blocks
            if type(item2) == pygame.rect.Rect:
                if item2.collidepoint(pos) and self.select is None:
                    self.craft_bag = list([[None for __ in range(3)] for _ in range(3)])
                    self.craft_lvl = list([[None for __ in range(3)] for _ in range(3)])
                    self.craft_blocks = list([[None for __ in range(3)] for _ in range(3)])
                    self.craft_bonus = list([[[None, None] for __ in range(3)] for _ in range(3)])
                    self.craft_bonuslvl = list([[[None, None] for __ in range(3)] for _ in range(3)])
                    sele = self.select
                    sele2 = self.selectlvl
                    sele3 = self.selectbonus
                    sele4 = self.selectbonuslvl
                    self.select = self.craft_result_bag
                    self.selectlvl = self.craft_result_lvl
                    self.selectbonus = self.craft_result_bonus
                    self.selectbonuslvl = self.craft_result_bonuslvl
                    self.craft_result_bag = sele
                    self.craft_result_lvl = sele2
                    self.craft_result_bonus = sele3
                    self.craft_result_bonuslvl = sele4

        flag = self.craft_bag[0][0]
        flagb = self.craft_lvl[0][0]
        flog = 1
        for ind1, i in enumerate(self.craft_bag):
            for ind2, j in enumerate(i):
                if flag != j and flagb != self.craft_bonus[ind1][ind2]:
                    flog = 0
        if flag is None: flog = 0
        if flog:
            self.craft_result_bag = flag
            self.craft_result_lvl = flagb + 1


def fresh():
    pass
