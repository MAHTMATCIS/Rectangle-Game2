# coding:utf-8
######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import json
import joystick
import pygame.gfxdraw
import sys
from math import *
import ctypes
import win32api
import multiprocessing
import time as timetime

import pygame.freetype
from pygame.display import get_active
import pygetwindow

from map import *
from items import *
import random
import items
import setting
from contact import deathmessage, pausemessage, renderdistance, waitmessage, test2

from base import *
from font import *

from OpenGL.GL import *
from OpenGL.GLU import *

score = Numbers(0)
difficult = Numbers(1)
pondDamage = Numbers(5)
ind = Numbers(0)
user32 = ctypes.windll.user32
Shcore = ctypes.windll.Shcore
random.seed(contact.seed if contact.seed != 'random' else time.time())

multiprocessing.freeze_support()

# 绘制线段的函数
def draw_line(screen, start, end, color):
    return pygame.draw.line(screen, color, start, end, 2)


#

def getrandomtick():
    return randint(int(20 / contact.randomtickspeed), int(200 / contact.randomtickspeed))


framerate = 0
crps = 0
fps = contact.FPS
tps = contact.tick


def showFPS(clock, surface, to, clock2, clock3):
    global framerate, fps, tps, crps
    if framerate < to // 5:
        framerate += 1
    else:
        framerate = 0
        fps = clock.get_fps()
        tps = clock2.get_fps()
        crps = clock3.get_fps()
    fps_text = "FPS: {:.2f}/{}".format(fps, to)
    if fps / to < 0.3:
        color = (255, 0, 0)
    elif fps / to < 0.5:
        color = (255, 200, 0)
    elif fps / to < 0.7:
        color = (200, 200, 0)
    else:
        color = (0, 200, 0)
    tps_text = "TPS: {:.2f}/{}".format(tps, contact.tick)
    if tps / contact.tick < 0.3:
        color1 = (255, 0, 0)
    elif tps / contact.tick < 0.5:
        color1 = (255, 200, 0)
    elif tps / contact.tick < 0.7:
        color1 = (200, 200, 0)
    else:
        color1 = (0, 200, 0)

    crps_text = "CRPS: {:.2f}/{}".format(crps, contact.rectick)
    if crps / contact.rectick < 0.3:
        color2 = (255, 0, 0)
    elif crps / contact.rectick < 0.5:
        color2 = (255, 200, 0)
    elif crps / contact.rectick < 0.7:
        color2 = (200, 200, 0)
    else:
        color2 = (0, 200, 0)
    arial.render_to(surface, (5, 5), fps_text, color)
    arial.render_to(surface, (5, 25), tps_text, color1)
    arial.render_to(surface, (5, 45), crps_text, color2)


class ShowArrow:
    def __init__(self):
        self.line = None

    def fresh(self, screen, center, pos):
        self.line = draw_line(screen, center, (pos[0], pos[1]), (0, 0, 0))


def getwin(hdc):
    for i in pygetwindow.getAllWindows():
        if i._hWnd == hdc['window']:
            return [i.left, i.top]


class MainWindow:
    def initmouse(self):
        if not contact.injoystick:
            if self.fullscreen == 0:
                win32api.SetCursorPos((self.center[0] + self.relcenter[0] + 8, self.center[1] + self.relcenter[1] + 31))
            else:
                win32api.SetCursorPos((self.center[0], self.center[1]))

    def summon(self):
        if self.stopsummon:
            return
        if len(self.elst) < contact.maxelsecount:
            elss = Else(self.surface, randint(-1000, self.size[0] + 1000), randint(-1000, self.size[1] + 1000),
                        forge=(230, 0, 0), size=int(50 * log(difficult.num / 2 + 1, 2)) + 25, center=self.center,
                        speed=uniform(1.0, 1.5) * (log10(int(difficult.num * 2 + 1))) + 1)
            elss.max_health = elss.health = randint(10, 50) * difficult.num
            elss.image = image.raw['else']
            elss.damage = randint(1, 3) * difficult.num
            if not elss.is_in(self.player):
                self.elst.append(elss)

    def rerender_image(self, *args, **kwargs):
        for i in self.ilst:
            i.update(*args, **kwargs)

    def fresh(self):
        posabs = self.posabs
        if injoystick:
            pygame.mouse.set_visible(1)
        self.frame += 1
        self.pos.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed)
        self.rerender_image(-self.mouse[0] * contact.mousespeed + posabs[0],
                            posabs[1] - self.mouse[1] * contact.mousespeed, self.scale, self.center)
        for i in self.map:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center, self.map, self.pos)
        self.player.update(*posabs, scale=self.scale, center=self.center, mouse=(
            -self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed))

        for i in self.dlst:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center)

        for i in self.items:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center)
        for i in self.elst:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     scale=self.scale, center=self.center, lst=self.elst, score=score, numlst=self.nlst, dlst=self.dlst,
                     diff=difficult, items=self.items)
        for i in self.nlst:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center)
        for i in self.plst:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center)
        self.bag.update(ind.num, self.tick, self.player, self.elst, self.plst, ind);
        self.bag.sizey = self.center[1] * 2 - 100
        for i in self.extra:
            i.update(-self.mouse[0] * contact.mousespeed + posabs[0], posabs[1] - self.mouse[1] * contact.mousespeed,
                     self.scale, self.center)
        if self.pause:
            for i in self.plst:
                i.power = [0, 0]
        self.mouse = [0, 0]
        if injoystick:
            self.joy.update(+400, self.center[1] * 2 - 200)
        ##################################################################
        if test2:
            if self.player.health > 40:
                ramp = 40
            elif self.player.health > 20:
                ramp = 20
            elif self.player.health > 10:
                ramp = 5
            elif self.player.health > 5:
                ramp = 5
                self.surface = pygame.transform.grayscale(self.surface, self.surface)
            else:
                ramp = 5
                self.surface = pygame.transform.laplacian(self.surface, self.surface)
            if self.randomtick is not None:
                if self.frame % ramp == 0:
                    self.surface.fill((0, 0, 0))
                if self.randomtick != 0:
                    return
                self.surface = pygame.transform.laplacian(self.surface, self.surface)

    def tickadd(self, tick):  #   相机运动与tick运动
        t = timetime.time()
        if tick % 10 == 0 and not self.ismaprefreshing.num:
            self.map.fresh(self.surface, self.center, self.pos, self.ismaprefreshing)
        if self.randomtick is None or self.randomtick < 0:
            self.randomtick = getrandomtick()
            self.summon()
        else:
            self.randomtick -= 1
        self.rendermap = (time.time() - t)

        win = getwin(pygame.display.get_wm_info())  # 获取中心点
        self.relcenter = win

        t = timetime.time()
        for i in self.dlst:
            i.tick(tick, self.dlst)
        self.renderd = (time.time() - t)
        t = timetime.time()
        for i in self.elst:
            i.testin([self.player, *self.player.flst1, *self.player.flst2, *self.player.flst3], self.elst, self.nlst)
        self.rendere = (time.time() - t)
        t = timetime.time()
        for i in self.nlst:
            i.tick(self.nlst)
        self.rendern = (time.time() - t)
        t = timetime.time()
        for i in self.elst:
            i.tick([self.player, *self.player.flst1, *self.player.flst2,
                    *self.player.flst3] if self.life and not self.pause else [])
        self.rendere += (time.time() - t)
        t = timetime.time()
        for i in self.plst:
            i.tick(self.player, self.plst)
            i.colliderect(self.elst, self.plst, self.nlst, self.extra)
        self.renderp = (time.time() - t)

        t = timetime.time()
        for i in self.extra:
            i.tick(self.extra)
        self.renderextra = (time.time() - t)

        t = timetime.time()
        for i in self.ilst:
            i.tick()
        self.renderi = (time.time() - t)

        for i in self.items:
            i.tick(self.player, self.bag, self.items, score)

        if self.player.islife():
            self.life = 0
            return
        self.player.addtick(tick, self.plst, self.elst, pondDamage.num, self.dlst, ind)

        self.posabs = [self.posabs[0] / contact.cameraspeed, self.posabs[1] / contact.cameraspeed]
        posabs = ((self.center[0] - self.player.x) / contact.cameraspeed + self.mouse[0] * contact.mousespeed,
                  (self.center[1] - self.player.y) / contact.cameraspeed + self.mouse[1] * contact.mousespeed)
        self.posabs[0] += posabs[0]
        self.posabs[1] += posabs[1]

    def addrecv(self):
        for i in self.elst:
            i.recv()
        for i in self.plst:
            i.recv()

    def read(self):
        try:
            with open(self.savefile) as f:
                global seed
                worldinfo = json.load(f)
                self.bag.bag = worldinfo['self.bag.bag']
                self.bag.bonus = worldinfo['self.bag.bonus']
                self.bag.lvl = worldinfo['self.bag.lvl']
                self.bag.bonuslvl = worldinfo['self.bag.bonuslvl']
                items.items = worldinfo['items.items']
                items.lvl = worldinfo['items.lvl']
                items.bonus = worldinfo['items.bonus']
                items.bonuslvl = worldinfo['items.bonuslvl']
                difficult.num = worldinfo['difficult']
                seed = worldinfo['seed']
                score.num = worldinfo['score']
                self.player.health = worldinfo['self.player.health']
                self.player.max_health = worldinfo['self.player.max_health']
        except:
            pass

    def save(self):
        with open(self.savefile, 'w') as f:
            worldinfo = {}
            worldinfo['self.bag.bag'] = self.bag.bag
            worldinfo['self.bag.bonus'] = self.bag.bonus
            worldinfo['self.bag.lvl'] = self.bag.lvl
            worldinfo['self.bag.bonuslvl'] = self.bag.bonuslvl
            worldinfo['items.items'] = items.items
            worldinfo['items.lvl'] = items.lvl
            worldinfo['items.bonus'] = items.bonus
            worldinfo['items.bonuslvl'] = items.bonuslvl
            worldinfo['difficult'] = difficult.num
            worldinfo['seed'] = seed
            worldinfo['score'] = score.num
            if self.player.health <= 0:
                worldinfo['self.player.health'] = self.player.max_health
            else:
                worldinfo['self.player.health'] = self.player.health
            worldinfo['self.player.max_health'] = self.player.max_health
            json.dump(worldinfo, f, check_circular=1)



    def __init__(self):
        self.savefile = contact.savefile
        self.renderi = 0
        self.renderextra = 0
        self.renderp = 0
        self.rendern = 0
        self.rendere = 0
        self.renderd = 0
        self.rendermap = 0
        self.debug = 0
        global win2, renderdistance, randomtickspeed
        pygame.init()

        # const value
        self.vsync = contact.vsync
        self.depth = contact.depth
        self.scale = 1
        self.posabs = (0, 0)
        self.mouse = (0, 0)
        self.tick = 0
        self.frame = 0
        self.fullscreen = 0
        self.mousemoving = 0
        self.size = contact.size
        self.relsize = self.size
        self.FPS = contact.FPS
        self.clock = pygame.time.Clock()
        # /const value about game
        self.tickclock = pygame.time.Clock()
        self.recvclock = pygame.time.Clock()
        self.life = 1
        self.pause = 0
        self.loading = 1
        self.ismove = 1
        self.ismaprefreshing = Numbers(0)
        self.randomtick = None
        #const value

        self.surface = pygame.display.set_mode(tuple(contact.size),
                                               pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE, self.depth,
                                               vsync=self.vsync)


        #surface edition
        pygame.display.set_caption(contact.title, contact.icontitle)
        pygame.display.set_icon(contact.icon)
        pygame.mouse.set_visible(0)
        win2 = getwin(pygame.display.get_wm_info())  #获取中心点
        self.relcenter = win2
        self.center = self.surface.get_rect().center
        #surface setting
        if contact.fullscreen:
            self.fullscr()

        ####################ITEMS

        self.elst = []
        #self.elst.append(Else(self.surface,0,0,forge=(230,0,0),size=50,center=self.center,speed=200))
        self.player = Player(self.surface, self.center[0], self.center[1], forge=(230, 230, 230), center=self.center,
                             color2=(200, 100, 100))

        self.player.max_health = 50
        self.player.health = 50
        self.nlst = []
        self.plst = []
        self.ilst = []
        self.dlst = []
        self.extra = []
        self.items = []
        self.pos = Pos()
        self.map = Map()
        self.joy = joystick.JoyStick(self.surface, self.center[0] + 100, self.center[1] + 100)
        self.bag = Bag(self.surface, 20, self.center[1] * 2 - 100)
        self.map.fresh(self.surface, self.center, self.pos, Numbers(0))

        ####################

        #重置

        def addtick():
            try:
                while self.life:
                    if not self.loading and not self.pause:
                        self.tick += 1

                        self.tickadd(self.tick)
                    self.tickclock.tick(contact.tick)
            except:
                user32.MessageBoxA(0, traceback.format_exc().encode('gbk'), b'error', 0x10)

        def addrec():
            try:
                while self.life:
                    if not self.loading and not self.pause:
                        self.addrecv()
                    self.recvclock.tick(contact.rectick)
            except:
                user32.MessageBoxA(0, traceback.format_exc().encode('gbk'), b'error', 0x10)

        self.initmouse()
        self.settingwindow = None
        self.ticing = False
        self.stopsummon = False
        image.init2()
        pygame.mouse.set_visible(0)

        for i in range(1000):
            f = font.chin.size('BY `MAHTMATCIS`')[0]
            self.surface.fill((0, 0, 0))
            x = font.chin.render('BY `MAHTMATCIS`', 1, (255 * i // 1000, 255 * i // 1000, 255 * i // 1000))

            self.surface.blit(x, [self.center[0] - f // 2, self.center[1]])
            pygame.display.flip()
            time.sleep(0.001)
        for i in range(500, 0, -1):
            f = font.chin.size('BY `MAHTMATCIS`')[0]
            self.surface.fill((0, 0, 0))
            x = font.chin.render('BY `MAHTMATCIS`', 1, (255 * i // 500, 255 * i // 500, 255 * i // 500))
            self.surface.blit(x, [self.center[0] - f // 2, self.center[1]])
            pygame.display.flip()
            time.sleep(0.001)
        self.alpha = 255
        self.suf2 = pygame.Surface(self.size)
        self.suf2.fill((0, 0, 0))
        self.alp = 0
        self.bagopen = 0

        self.read()

        while True:
            self.surface.fill(contact.bg)
            if self.alpha >= 0:
                self.suf2.set_alpha(self.alpha)
                self.alpha //= 1.1

            elif self.alp == 0:
                self.alp = 1
                self.initmouse()

            self.fresh()
            self.mousedown = 0

            showFPS(self.clock, self.surface, self.FPS, self.tickclock, self.recvclock)

            arial.render_to(self.surface, (5, 65), 'Coin:' + str(score), (0, 0, 0))
            arial.render_to(self.surface, (5, 85), 'Difficult:' + str(difficult), (0, 0, 0))
            arial.render_to(self.surface, (5, 105), 'Spawning Speed:' + str(contact.randomtickspeed), (0, 0, 0))
            arial.render_to(self.surface, (5, 125),
                            'x,y:' + str(self.pos.x.__round__(3)) + ',' + str(self.pos.y.__round__(3)), (0, 0, 0))
            if self.debug:
                arial.render_to(self.surface, (5, 125), '---DEBUG OPEN---', (0, 0, 0))
                arial.render_to(self.surface, (5, 145), 'rederi:' + str(self.renderi), (0, 0, 0))
                arial.render_to(self.surface, (5, 165), 'redere:' + str(self.rendere), (0, 0, 0))
                arial.render_to(self.surface, (5, 185), 'redermap:' + str(self.rendermap), (0, 0, 0))
                arial.render_to(self.surface, (5, 205), 'rederd:' + str(self.renderd), (0, 0, 0))
                arial.render_to(self.surface, (5, 225), 'rederextra:' + str(self.renderextra), (0, 0, 0))
                arial.render_to(self.surface, (5, 245), 'redern:' + str(self.rendern), (0, 0, 0))

            ev = pygame.event.get()
            if self.alpha > 10:
                self.initmouse();
                ev = []

            for event in ev:

                if event.type == pygame.QUIT:
                    self.life = 0
                    pygame.quit()
                    sys.exit(-1)

                elif event.type == pygame.KEYDOWN:
                    print(event.key)

                    if event.key == pygame.K_F11 or event.key == 102:  # f11 or f
                        self.fullscr()
                    elif event.key == pygame.K_ESCAPE:
                        self.life = 0
                        self.save()
                        pygame.quit()
                        sys.exit(-1)
                    elif event.key == 1073742050:
                        self.ismove = not self.ismove
                        pygame.mouse.set_visible(self.ismove)
                        self.initmouse()
                    elif event.key == pygame.K_F2 or event.key == 120:  # f2 or x
                        self.stopsummon = not self.stopsummon
                    elif (event.key == pygame.K_F1 or event.key == 122) and self.ticing and self.life:
                        self.pause = not self.pause
                        pygame.mouse.set_visible(self.pause)
                        self.initmouse()
                        self.player.type = 0

                    elif event.key == 113 and not self.pause and self.life:  # q
                        if score.num >= 100:
                            score.num -= 100
                            self.player.addF1()
                    elif event.key == 119 and not self.pause and self.life:  # w
                        if score.num >= 1000:
                            score.num -= 1000
                            self.player.addF2()

                    elif event.key == 115 and not self.pause and self.life:  # s
                        if self.settingwindow is None:
                            self.pause = 1
                            if self.settingwindow is None or self.settingwindow.is_alive():
                                process = multiprocessing.Process(target=setting.Setting)
                                process.start()
                                self.settingwindow = process

                    elif event.key == 115:
                        self.save()

                    elif event.key == 116:
                        ch(self.scale)
                        self.scale *= 1.1
                    elif event.key == 121:
                        ch(self.scale)
                        self.scale /= 1.1

                    elif event.key == 113 and self.bagopen:  # q
                        self.bag.q(pygame.mouse.get_pos())

                    elif event.key == 105:  # i
                        difficult.num -= 0.5
                        difficult.num = round(difficult.num, 2)
                    elif event.key == 107:  # k
                        difficult.num += 0.5
                        difficult.num = round(difficult.num, 2)

                    elif event.key == 111:  # o
                        randomtickspeed -= 0.1
                    elif event.key == 108:  # l
                        randomtickspeed += 0.1

                    elif event.key == 106:  # j
                        if score.num >= 5000:
                            score.num -= 5000
                            self.player.health += 50
                            self.player.max_health += 50

                    elif event.key == 99:  # c
                        self.items.clear()
                    elif event.key == 100:  # d
                        for i in self.items:
                            i: Item
                            x1, y1 = self.player.self1.center
                            x2, y2 = i.x, i.y

                            x = (x2 - x1)
                            y = (y2 - y1)
                            z = math.sqrt(x ** 2 + y ** 2)

                            angle = (math.asin(y / z))
                            if contact.test1:
                                angle = uniform(0, 6.28)
                            speed = [math.cos(angle) * 20, -math.sin(angle) * 20]
                            if x2 >= x1:
                                speed[0] = -speed[0]
                            i.powered = speed

                    elif event.key == 101 and self.life and self.ticing:  # e
                        self.pause = not self.pause
                        self.bagopen = not self.bagopen
                        self.player.type = 0
                        if self.bagopen:
                            self.pause = 1
                        pygame.mouse.set_visible(self.pause)
                        self.initmouse()

                    elif event.key == 32 and not self.pause and self.life:
                        self.player.health += 1
                        nu = Num(self.surface, self.scale, self.center, -1, self.player.x, self.player.y)
                        self.nlst.append(nu)




                elif event.type == pygame.VIDEORESIZE and self.fullscreen == 0:  # 调整窗口大小
                    self.resize(event.size[0], event.size[1])


                elif event.type == pygame.ACTIVEEVENT and self.pause == 0:
                    print('pause')
                    self.pause = not self.pause
                    pygame.mouse.set_visible(self.pause)
                    self.initmouse()


                elif event.type == pygame.MOUSEMOTION and self.mousemoving == 0 and self.ismove == 1:
                    pos = event.pos
                    if injoystick:
                        self.joy.move(event.pos)
                    if self.ticing == 0 and self.pause == 0:
                        threading.Thread(target=addtick).start()  # about tick
                        threading.Thread(target=addrec).start()  # about tick
                        self.ticing = 1
                    if self.loading == 1:
                        self.pause = 0
                        self.loading = 0
                    if self.life and not self.pause:
                        if not injoystick:
                            self.move(event)

                    else:  #defeat
                        self.posabs = [0, 0]
                        self.mouse = [0, 0]
                        self.pause = 1
                        pygame.mouse.set_visible(1)
                        continue


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousedown = 1
                    if injoystick and self.mousedown:
                        self.joy.move(event.pos)
                    ch(self.scale)
                    if self.bagopen:
                        self.bag.click(event)
                    if event.button == 1 and not self.pause and self.life:
                        self.player.type = 1

                    elif event.button == 4:
                        ch(self.scale)
                        self.scale *= 1.1
                    elif event.button == 5:
                        ch(self.scale)
                        self.scale /= 1.1


                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mousedown = 0
                    if event.button == 1 and not self.pause and self.life:
                        self.player.type = 0

            if not self.ticing:
                f = font.chin.size(waitmessage)[0]
                x = font.chin.render(waitmessage, True, (0, 0, 0))
                x2 = font.chin.render(waitmessage, True, (255, 255, 255))
                self.surface.blit(x2, [self.center[0] - f // 2 + 2, self.center[1] + 55 + 2])
                self.surface.blit(x, [self.center[0] - f // 2, self.center[1] + 55])

            if self.stopsummon:
                f = font.chin.size('stopsummon')[0]
                x = font.chin.render('stopsummon', True, (0, 0, 0))
                x2 = font.chin.render('stopsummon', True, (255, 255, 255))
                self.surface.blit(x2, [self.center[0] - f // 2 + 2, self.center[1] + 55 + 2])
                self.surface.blit(x, [self.center[0] - f // 2, self.center[1] + 55])
            if not self.life:
                f = font.chin.size(deathmessage)[0]
                x = font.chin.render(deathmessage, True, (255, 0, 0))
                x2 = font.chin.render(deathmessage, True, (255, 255, 255))
                self.surface.blit(x, [self.center[0] - f // 2, self.center[1] + 10])
                self.surface.blit(x2, [self.center[0] - f // 2 + 2, self.center[1] + 10 + 2])
            elif self.pause and not self.bagopen:
                f = font.chin.size(pausemessage)[0]
                x = font.chin.render(pausemessage, True, (255, 0, 0))
                x2 = font.chin.render(pausemessage, True, (255, 255, 255))
                self.surface.blit(x2, [self.center[0] - f // 2 + 2, self.center[1] + 10 + 2])
                self.surface.blit(x, [self.center[0] - f // 2, self.center[1] + 10])

            elif self.bagopen:
                self.bag.background(self.center)
                self.bag.moving(pos)

            x = font.small.render('by MAHTMATCIS,FOLLOW and SUBSCRIBE!', True, (0, 0, 0))
            x2 = font.small.render('by MAHTMATCIS,FOLLOW and SUBSCRIBE!', True, (255, 255, 255))
            self.surface.blit(x2, [12, self.center[1] * 2 - 20 + 2])
            self.surface.blit(x, [10, self.center[1] * 2 - 20])
            self.surface.blit(self.suf2, (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)
            if injoystick:
                self.movejoystick()

    def resize(self, width, height):
        window_width = width
        window_height = height
        self.size = [window_width, window_height]
        self.surface = pygame.display.set_mode((window_width, window_height),
                                               pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE, self.depth,
                                               vsync=self.vsync)
        self.center = self.surface.get_rect().center
        self.initmouse()
        win = getwin(pygame.display.get_wm_info())  #获取中心点
        self.relcenter = win

    def fullscr(self):
        if not self.fullscreen:
            self.relsize = self.size
            print(contact.fullsize)
            self.size = contact.fullsize
            self.surface = pygame.display.set_mode(self.size,
                                                   pygame.FULLSCREEN,
                                                   self.depth, vsync=self.vsync)
        else:
            self.size = self.relsize
            print(self.relsize)
            self.surface = pygame.display.set_mode(self.relsize,
                                                   pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE, self.depth,
                                                   vsync=self.vsync)
        self.center = self.surface.get_rect().center
        self.fullscreen = not self.fullscreen
        self.initmouse()

    def move(self, event):
        xabs = event.pos[0] - self.center[0]
        yabs = event.pos[1] - self.center[1]
        posabs = (xabs, yabs)
        self.mousemoving = 1
        self.initmouse()
        self.mouse = posabs
        self.mousemoving = 0

    def movejoystick(self):
        self.mouse = self.joy.upd(self.center[0] + 100, self.center[1] + 100)


def main():
    if contact.noResolution:
        user32.SetProcessDPIAware()
        if not contact.noWarning:
            x = user32.MessageBoxA(0,
                                   "You are using the no resolution (ignoring system scaling) mode, which may cause "
                                   "unforeseen errors! Please consider carefully!\n\nSet 'noWarning' to 'true' in "
                                   "'conf.toml' and ignore this "
                                   "prompt.\n\n你在使用无分辨率（忽略系统缩放）模式，这可能会导致无法预料的错误！请谨慎考虑！\n\n在“conf.toml”里将“noWarning"
                                   "”设为“true”忽略本提示。\n\nDo you want to continue playing?  是否继续游戏？".encode(
                                       'gbk'), (contact.title + ': Warning!   警告！').encode('gbk'), 0x31)
            if x == 2:
                sys.exit(-1)

    try:
        main = MainWindow()
    except SystemExit:
        pass
    except:
        user32.MessageBoxA(0, traceback.format_exc().encode('gbk'), b'error', 0x10)


if __name__ == '__main__':
    main()
