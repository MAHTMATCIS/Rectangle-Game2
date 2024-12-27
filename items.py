######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import pygame

import font
import image
import item_info
from base import Numbers
from item_info import rawall

pygame.init()
image.init()
# todo 这里用来搞物品
weapon='none'

weapondict = {}
for i in rawall['weapon_type']:
    weapondict[i] = image.raw['weapon.' + i]
items = ['puncture', 'puncture', 'puncture']
lvl = [4, 4, 4]
itemdict = {}
for i in rawall['item_type']:
    itemdict[i] = image.raw['item.' + i]

class Bag:
    def __init__(self,surface,sizex,sizey):
        self.surface:pygame.Surface=surface
        self.sizex=sizex;self.sizey=sizey
        self.tick = 0

    def update(self, ind, tick, player, elst, plst, indx):

        ind%=len(items)
        x=font.normal.render('Weapon(武器): '+weapon,1,'black')
        self.surface.blit(x,(self.sizex+2,self.sizey-153))
        x=font.normal.render('Weapon(武器): '+weapon,1,'white')
        self.surface.blit(x,(self.sizex,self.sizey-155))
        pygame.draw.rect(self.surface, 'black', ((self.sizex-8, self.sizey - 118), (70, 70)), 3, 10)
        pygame.draw.rect(self.surface, 'white', ((self.sizex-10, self.sizey - 120), (70, 70)), 3, 10)
        self.surface.blit(weapondict[weapon], (self.sizex, self.sizey-110))

        x = font.normal.render('Items(物品栏): ' + str(lvl[ind]) + ' ' + items[ind], 1, 'black')
        self.surface.blit(x,(self.sizex+2,self.sizey-43))
        x = font.normal.render('Items(物品栏): ' + str(lvl[ind]) + ' ' + items[ind], 1, 'white')
        self.surface.blit(x,(self.sizex,self.sizey-45))
        pygame.draw.rect(self.surface, 'black', ((self.sizex-8, self.sizey - 8), (60*len(items)+10, 70)), 3, 10)
        pygame.draw.rect(self.surface, 'white', ((self.sizex-10, self.sizey - 10), (60*len(items)+10, 70)), 3, 10)
        flag = 0
        timesleep = eval(item_info.raw[items[ind]]['timesleep'])

        if tick - self.tick > timesleep and player.type == 1:
            self.tick = tick
            if len(elst) > 0:
                if type(indx) == Numbers:
                    player.summon_pond(plst, elst, typ=items[indx.num % items.__len__()],
                                       lvl=lvl[indx.num % lvl.__len__()])
                    indx.num += 1
        scale = (tick - self.tick) / timesleep

        for index,item in enumerate(items):
            if ind==index:pygame.draw.rect(self.surface,'black',((self.sizex+index*60-3,self.sizey-3),(60,60)),3,10)
            if ind == index:
                pygame.draw.rect(self.surface, 'white', ((self.sizex + index * 60 - 5, self.sizey - 5), (60, 60)), 3,
                                 10)
                pygame.draw.rect(self.surface, 'white',
                                 (((self.sizex + index * 60 - 5), self.sizey - 5 + 60 * scale), (60, 60 * (1 - scale))))
            x = font.small.render(str(lvl[index]), True, (0, 0, 0))
            x2 = font.small.render(str(lvl[index]), True, (255, 255, 255))
            self.surface.blit(itemdict[item],(self.sizex+index*60,self.sizey))
            self.surface.blit(x, (self.sizex + index * 60 + 2, self.sizey + 2))
            self.surface.blit(x2, (self.sizex + index * 60, self.sizey))

def fresh():
    pass