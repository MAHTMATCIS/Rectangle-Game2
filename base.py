######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import math
from random import randint, uniform
from traceback import print_exc

import pygame
import pygame.freetype

import item_info
from contact import maxpondcount

pygame.freetype.init()
import contact
import font
import image

image.init()


class Entity:
    def __init__(self, surface: pygame.Surface, x, y, size=100, forge=(0, 0, 0, 0), width=2, border=(0, 0, 0, 0),
                 center=(0, 0), scale=1, notupd=0):
        self.ima = 1
        self.image2 = None
        self.self2 = None
        self.self1 = None
        self.healtht = None
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.forge = forge
        self.width = width
        self.border = border
        self.scale = scale
        self.center = center
        self.type = 0
        self.power = [0, 0]
        self.max_health = 0
        self.health = 0
        self.life = 1
        self.flst1 = []
        self.flst2 = []
        self.flst3 = []
        self.bar = Bar(surface, x - 60, y - 70, 120, 10, (0, 255, 0), 'black', 2)
        self.showbar = 1
        self.image = None
        if not notupd:
            self.update(center=center, scale=scale)

    def addF1(self):
        if len(self.flst1) > contact.maxfriendcount:
            return
        center = self.x, self.y
        f1 = Friend(self.surface, center[0], center[1], forge=(50, 50, 230), center=center, color2=(200, 100, 100),
                    player=self, size=40, type=1)
        f1.health = 30
        f1.max_health = 30
        self.flst1.append(f1)

    def addF2(self):
        if len(self.flst2) > contact.maxfriendcount:
            return
        center = self.x, self.y
        f2 = Friend(self.surface, center[0], center[1], forge=(100, 0, 230), center=center, color2=(150, 150, 100),
                    player=self, size=50, type=2)
        f2.health = 30
        f2.max_health = 30
        self.flst2.append(f2)

    def islife(self):
        return self.health <= 0

    def is_in(self, x):

        return self.self1.colliderect(x.self1)

    def distance(self, x, y=None):
        if y is not None:
            x1 = x
            x2 = y
        else:
            x1 = self.x - x.x
            x2 = self.y - x.y
        return (x1 ** 2 + x2 ** 2) ** 0.5

    def update(self, x=0, y=0, scale=1, center=(0, 0), mouse=(0, 0), chima=-1):
        self.center = center
        self.x += x
        self.y += y
        if self.showbar:
            self.bar.update(x, y, center, scale, self.health, self.max_health)
        flg = 0
        if self.scale != scale:
            self.scale = scale
            flg = 1
        self.self2 = pygame.draw.rect(self.surface, self.forge if self.type == 0 else self.color2,
                                      [[(self.x - self.size // 2 - self.center[0]) * self.scale + self.center[0],

                                        (self.y - self.size // 2 - self.center[1]) * self.scale + self.center[1]],

                                       [int(self.size * self.scale), int(self.size * self.scale)]], self.size * 1000)

        self.self1 = pygame.draw.rect(self.surface, self.border,
                                      [[(self.x - self.size // 2 - self.center[0]) * self.scale + self.center[0],

                                        (self.y - self.size // 2 - self.center[1]) * self.scale + self.center[1]],

                                       [int(self.size * self.scale), int(self.size * self.scale)]], self.width)
        text = str(round(self.health, 3)) + "/" + str(self.max_health)
        size = font.arial.get_rect(text).size[0]
        if chima == -1:
            pass
        else:
            self.ima = chima
        if self.image is not None:
            if self.image2 is None:
                self.image2 = self.image
            if flg:
                self.image2 = pygame.transform.scale(self.image, (
                    self.ima * self.scale * self.image.get_rect().size[0] + 1,
                    self.ima * self.scale * self.image.get_rect().size[1] + 1))
            self.surface.blit(self.image2, ((self.x - self.size - self.center[0]) * self.scale + self.center[0],
                                            (self.y - self.size - self.center[1]) * self.scale + self.center[1]))
        self.healtht = font.arial.render_to(self.surface,
                                            [int((self.x - size / 2 - self.center[0]) * self.scale) + self.center[0],
                                             int((self.y - self.center[1] - self.size) * self.scale + self.center[1])],
                                            text)

        for i in self.flst1:
            i.update(x, y, scale, center, mouse)
        for i in self.flst2:
            i.update(x, y, scale, center, mouse)


class Image(Entity):
    def __init__(self, *args, **kwargs):
        image = kwargs['image']
        del kwargs['image']
        self.scr = uniform(0.5, 2.0)
        super().__init__(*args, **kwargs, notupd=1)
        self.image2 = image
        self.image = image

        self.scale = 0.1
        self.update()

    def update(self, x=0, y=0, scale=1, center=(0, 0), mouse=(0, 0), add=(0, 0)):
        self.x += x
        self.y += y
        if self.scale != scale:
            self.scale = scale
            self.image2 = pygame.transform.scale(self.image, (self.scale * self.scr * self.image.get_rect().size[0] + 1,
                                                              self.scale * self.scr * self.image.get_rect().size[
                                                                  1] + 1))

        self.surface.blit(self.image2, (
            (self.x - center[0]) * self.scale + center[0] + add[0],
            (self.y - center[1]) * self.scale + center[1] + add[1]))

    def tick(self):
        pass


class Numbers:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)


class Num:
    def __init__(self, surface, scale, center, num, x, y, typ=0):
        self.surface = surface
        self.scale = scale
        self.center = center
        self.num = num
        self.x = x
        self.y = y
        self.typ = typ
        if self.num < 2:
            self.color = (100, 200, 0)
        elif self.num < 5:
            self.color = (100, 100, 0)
        elif self.num < 20:
            self.color = (255, 0, 0)
        else:
            self.color = (150, 0, 0)
        self.time = 20

    def islife(self):
        return self.time <= 0

    def tick(self, lst):
        self.y -= 5
        if self.islife():
            lst.remove(self)
        self.time -= 1

    def update(self, x=0, y=0, scale=1, center=(0, 0), ):
        self.center = center
        self.scale = scale
        self.x += x
        self.y += y
        x = self.x
        y = self.y
        text = str(-self.num)
        size = font.arial.get_rect(text).size[0]
        try:
            font.arial.render_to(self.surface, [int((x - size / 2 - self.center[0]) * self.scale) + self.center[0] + 2,
                                                int((y - self.center[1]) * self.scale + self.center[1]) + 2], text,
                                 (255, 255, 255))
            font.arial.render_to(self.surface, [int((x - size / 2 - self.center[0]) * self.scale) + self.center[0],
                                                int((y - self.center[1]) * self.scale + self.center[1])], text,
                                 self.color)
        except:
            pass


class Pond(Entity):
    def __init__(self, *args, **kwargs):
        # todo 解析类型
        self.ticks = 0
        self.speed = [0, 0]
        self.type = kwargs['type']
        del kwargs['type']
        self.typ = kwargs['typ']
        del kwargs['typ']
        self.lvl = kwargs['lvl']
        del kwargs['lvl']
        self.target = kwargs['target']
        del kwargs['target']
        self.bonus = kwargs['bonus']
        del kwargs['bonus']
        self.bonuslvl = kwargs['bonuslvl']
        del kwargs['bonuslvl']
        try:
            anglefix = kwargs['anglefix']
            del kwargs['anglefix']
        except:
            anglefix = 0

        self.sp = 5
        kwargs['size'] = 20
        kwargs['forge'] = (255, 255, 255)
        self.damage = 3
        for key, val in item_info.raw.items():
            if self.typ == key:
                kwargs['forge'] = val['forge']
                self.damage += eval(val['damage'])
                kwargs['size'] = val['size']
                self.sp = val['sp']
        for key, val in item_info.bonusInfo.items():
            for index, i in enumerate(self.bonus):
                if i == key and i is not None:
                    self.damage += eval(val['damage'])

        super().__init__(*args, **kwargs)
        self.update(center=self.center, scale=self.scale)
        self.initspeed(anglefix)
        self.fun = [0, 0]

    def initspeed(self, anglefix=0):
        try:
            x1, y1 = self.target.self1.center
            x2, y2 = self.center

            x = (x2 - x1)
            y = (y2 - y1)
            z = math.sqrt(x ** 2 + y ** 2)

            angle = (math.asin(y / z)) + anglefix
            if contact.test1:
                angle = uniform(0, 6.28)
            self.speed = [math.cos(angle), -math.sin(angle)]
            if x2 >= x1:
                self.speed[0] = -self.speed[0]
        except:
            pass

    def is_in(self, x):
        return self.self1.colliderect(x.self1)

    def colliderect(self, lst, plst, numlst, anima):
        for i in lst:
            if self.is_in(i):
                try:
                    if self.typ != 'puncture':
                        plst.remove(self)
                    if self.typ == "phosphor":

                        for j in range(1):
                            p = Pond(  # phosphor
                                self.surface, self.x, self.y, typ='phosphor', lvl=1, center=self.self1.center,
                                scale=self.scale,
                                type=1, target=self.target
                            )
                            p.type = 1
                            plst.append(p)
                    if self.typ == "lightning":
                        sor = sorted(lst, key=self.distance)
                        for i in range(self.lvl + 2):
                            if self.distance(sor[i]) < self.lvl * 100 + 200:
                                ani = LightAnim(self.surface, self.x, self.y, end=sor[i])
                                ani.ticks = 10
                                anima.append(ani)
                                sor[i].health -= self.damage
                                num = Num(self.surface, self.scale, self.center, self.damage, sor[i].x, sor[i].y)
                                numlst.append(num)
                        return

                    i.health -= self.damage
                    num = Num(self.surface, self.scale, self.center, self.damage, self.x, self.y)
                    numlst.append(num)
                except:
                    pass

    def tick(self, player, plst):
        self.ticks += 1
        if self.distance(player) > contact.pondmaxdis:
            if self.typ != 'puncture':
                plst.remove(self)

    def recv(self):
        self.x += self.power[0] + self.fun[0]
        self.y += self.power[1] + self.fun[1]
        self.power[0] += self.speed[0] * self.sp
        self.power[1] += self.speed[1] * self.sp
        self.power = [self.power[0] / contact.holval, self.power[1] / contact.holval]

    def update(self, x=0, y=0, scale=1, center=(0, 0)):
        self.x += x
        self.y += y
        self.center = center
        self.scale = scale
        forge = self.forge
        if self.typ == 'lightning' and self.ticks % 2 == 1: forge = '#99D9EA'
        self.self2 = pygame.draw.rect(self.surface, forge,
                                      [[(self.x - self.size // 2 - self.center[0]) * self.scale + self.center[0],

                                        (self.y - self.size // 2 - self.center[1]) * self.scale + self.center[1]],

                                       [int(self.size * self.scale), int(self.size * self.scale)]], self.size * 1000)

        self.self1 = pygame.draw.rect(self.surface, self.border,
                                      [[(self.x - self.size // 2 - self.center[0]) * self.scale + self.center[0],

                                        (self.y - self.size // 2 - self.center[1]) * self.scale + self.center[1]],

                                       [int(self.size * self.scale), int(self.size * self.scale)]], self.width)


class Animation(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticks = 0

    def tick(self, anim):
        self.ticks -= 1
        if self.ticks < 0:
            anim.remove(self)


class LightAnim(Animation):
    def __init__(self, *args, **kwargs):
        self.end = kwargs['end']
        del kwargs['end']
        self.endx = self.end.x
        self.endy = self.end.y
        self.ticks = 0
        super().__init__(*args, **kwargs)

    def update(self, x=0, y=0, scale=1, center=(0, 0), mouse=(0, 0)):
        self.x += x
        self.y += y
        self.endx += x
        self.endy += y
        self.scale = scale
        self.center = center
        self.self1 = pygame.draw.line(self.surface, "#73FBFD", (
            (self.x - self.center[0]) * self.scale + self.center[0],
            (self.y - self.center[1]) * self.scale + self.center[1]
        ), (
                                          (self.endx - self.center[0]) * self.scale + self.center[0],
                                          (self.endy - self.center[1]) * self.scale + self.center[1]
                                      ), self.ticks // 2)


class Ptr:
    def __init__(self, surface, scale, center):
        self.surface = surface
        self.scale = scale
        self.center = center
        self.size = 0
        self.angle = 0
        self.color = (0, 0, 0)

    def tick(self, size, angle, color):
        self.size = size
        self.angle = angle
        self.color = color

    def update(self):
        angle = self.angle
        color = self.color
        size = self.size
        self.updat(self.center, math.sin(angle) * size, color, size)

    def updat(self, posfrom, posto, color, size):
        pygame.draw.lines(self.surface, color, True, [posfrom, posto], size)


class Player(Entity):
    def __init__(self, *args, **kwargs):
        self.color2 = kwargs['color2']
        del kwargs['color2']

        super().__init__(*args, **kwargs)
        self.bar.forge = 'blue'
        self.bar.back = 'white'

    def get_near(self, lst):
        cnt = math.inf
        targe = None
        for i in lst:
            base = self.distance(i)
            if cnt > base:
                targe = i
                cnt = base
        return targe

    def update(self, x=0, y=0, scale=1, center=(0, 0), mouse=(0, 0)):
        super().update(x, y, scale, center, mouse)

    def addtick(self, tick, plst, elst, ponddam, dlst, ind):
        if tick % 20 == 0 and self.health < self.max_health:
            self.health += 1
        for i in self.flst1:
            i.addtick(tick, plst, elst, self.flst1, ponddam, dlst)
        for i in self.flst2:
            i.addtick(tick, plst, elst, self.flst2, ponddam, dlst)

    def summon_pond(self, plst, elst, types=1, pondDamage=3, typ='normal', lvl=1, bonus=None, bonuslvl=None):
        if bonus is None:
            bonus = [None, None]
        if bonuslvl is None:
            bonuslvl = [None, None]
        ta = self.get_near(elst)
        if len(plst) < maxpondcount:
            if typ == 'puncture':
                for i in range(-lvl + 1, lvl):
                    p = Pond(  # puncture
                        self.surface, self.x, self.y, typ=typ, lvl=lvl, center=self.self1.center, scale=self.scale,
                        type=1, target=ta, anglefix=i / 5, bonus=bonus, bonuslvl=bonuslvl
                    )
                    p.type = types
                    plst.append(p)
            if typ == 'phosphor':
                for i in range(5):
                    p = Pond(  # summon phosphor
                        self.surface, self.x, self.y, typ=typ, lvl=lvl, center=self.self1.center, scale=self.scale,
                        type=1, target=ta, anglefix=uniform(0., 6.28), bonus=bonus, bonuslvl=bonuslvl
                    )
                    p.type = types
                    plst.append(p)
            else:
                p = Pond(
                    self.surface, self.x, self.y, typ=typ, lvl=lvl, center=self.self1.center, scale=self.scale,
                    type=1, target=ta, bonus=bonus, bonuslvl=bonuslvl
                )
                p.type = types
                plst.append(p)


class Death(Entity):
    def __init__(self, *args, **kwargs):
        self.selfx = None
        self.alpha = 155
        self.tic = None
        self.rot = randint(0, 360)
        super().__init__(*args, **kwargs)

    def tick(self, tick, dlst):
        if self.tic is None:
            self.tic = tick
        self.alpha = 155 + self.tic * 2 - tick * 2
        if self.alpha <= 0:
            dlst.remove(self)

    def update(self, x=0, y=0, scale=1, center=(0, 0)):
        self.center = center
        self.scale = scale
        self.x += x
        self.y += y
        self.self2 = pygame.Surface((int(self.size * self.scale), int(self.size * self.scale)))
        self.self2.set_alpha(self.alpha)
        pygame.draw.rect(self.self2, self.forge, [[0, 0],

                                                  [int(self.size * self.scale), int(self.size * self.scale)]])
        pygame.draw.rect(self.self2, self.border, [[0, 0],

                                                   [int(self.size * self.scale), int(self.size * self.scale)]],
                         self.width)
        try:
            self.surface.blit(self.self2, [(self.x - self.size // 2 - self.center[0]) * self.scale + self.center[0],

                                           (self.y - self.size // 2 - self.center[1]) * self.scale + self.center[1]])
        except pygame.error:
            pass


class Item(Entity):
    pass


class Else(Entity):
    def __init__(self, *args, **kwargs):
        self.speed = kwargs['speed']
        self.damage = 1
        del kwargs['speed']
        super().__init__(*args, **kwargs)
        self.showbar = 1
        self.bar.forge = 'red'

    def testin(self, a, lst, numlst):

        for i in a:
            if self.is_in(i):
                self.health -= self.damage
                i.health -= self.damage
                num = Num(self.surface, self.scale, self.center, self.damage, self.x, self.y)
                numlst.append(num)

    def tick(self, target):
        self.power = [self.power[0] / contact.holval, self.power[1] / contact.holval]

        cnt = math.inf
        targe = None
        for i in target:
            i: Player
            center1 = i.self1.center
            center2 = self.self1.center
            xwidth = abs(center1[0] - center2[0])
            ywidth = abs(center1[1] - center2[1])
            base = math.sqrt(xwidth ** 2 + ywidth ** 2)
            if cnt > base:
                targe = i
                cnt = base
        if targe:
            if targe.self1.center[0] < self.self1.center[0]:
                self.power[0] -= self.speed
            else:
                self.power[0] += self.speed
            if targe.self1.center[1] < self.self1.center[1]:
                self.power[1] -= self.speed
            else:
                self.power[1] += self.speed

    def recv(self):

        self.x += self.power[0]
        self.y += self.power[1]
        self.bar.x += self.power[0]
        self.bar.y += self.power[1]

    def update(self, x=0, y=0, scale=1, center=(0, 0), lst=None, score=None, numlst=None, dlst=None, diff=None):
        super().update(x, y, scale, center, chima=self.size / 50)
        if self.islife():
            try:
                death = Death(self.surface, self.x, self.y, self.size, self.forge, self.width, self.border, self.center,
                              self.scale)
                dlst.append(death)
                lst.remove(self)
                score.num += diff.num
            except:
                pass


class Bar:
    def __init__(self, surface, x, y, xto, yto, forge, back, width):
        self.surface: pygame.Surface = surface
        self.x = x
        self.y = y
        self.xto = xto
        self.yto = yto
        self.forge = forge
        self.back = back
        self.width = width

    def update(self, x, y, center, scale, val, maxv):
        self.x += x
        self.y += y
        recv = val / (maxv + 0.1)
        if recv < 0: recv = 0
        surface = pygame.Surface((self.xto * scale + self.width + 0.1, self.yto * scale + self.width))
        surface.fill(self.back)
        surface.set_alpha(120)
        surface2 = pygame.Surface(((self.xto * scale) * recv + 0.1, self.yto * scale))
        surface2.fill(self.forge)
        surface2.set_alpha(190)
        self.surface.blit(surface, ((self.x - center[0]) * scale + center[0], (self.y - center[1]) * scale + center[1]))
        self.surface.blit(surface2, ((self.x + self.width // 2 - center[0]) * scale + center[0],
                                     (self.y + self.width // 2 - center[1]) * scale + center[1]))


class Friend(Player):
    def __init__(self, *args, **kwargs):
        self.player = kwargs['player']
        del kwargs['player']
        self.types = kwargs['type']
        del kwargs['type']
        super().__init__(*args, **kwargs)
        self.bar.forge = 'green'
        self.bar.back = 'black'
        self.pond = 'normal'

    def addtick(self, tick, plst, elst, flst=None, ponddam=3, dlst=None):
        pondspeed = 5 if self.types == 0 else 3 if self.types == 1 else 2
        if flst:
            if self.islife():
                flst.remove(self)
                death = Death(self.surface, self.x, self.y, self.size, self.forge, self.width, self.border, self.center,
                              self.scale)
                dlst.append(death)
        if tick % 20 == 0 and self.health < self.max_health:
            self.health += 1
        if tick % pondspeed == 0:
            if elst:
                self.summon_pond(plst, elst, 2 + self.types, ponddam)
                if self.types != 1:
                    super().addtick(1, plst, elst, ponddam, dlst, self.pond)

    def update(self, x=0, y=0, scale=1, center=(0, 0), mouse=(0, 0)):
        super().update(*mouse, scale, center)
