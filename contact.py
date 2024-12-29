######################################################################################################################################################################
#  /¯¯¯¯\¯\  /¯¯¯¯\¯\       /¯¯¯¯\¯\     |¯¯|¯|  |¯¯|¯| ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉  /¯¯¯¯\¯\  /¯¯¯¯\¯\      /¯¯¯¯\¯\     ⌈¯¯¯¯¯¯¯¯¯¯¯¯⌉`⌉    /¯¯¯¯¯¯¯|¯|  |¯¯|¯|   /¯¯¯¯¯¯|¯|  #
# /  /\  \ \/  /\  \ \     /  /\  \ \    |  | |  |  | | `¯¯¯¯⌉  ⌈¯⌈¯¯`¯` /  /\  \ \/  /\  \ \    /  /\  \ \    `¯¯¯¯⌉  ⌈¯⌈¯¯`¯`  /  / /¯¯¯¯`¯`  |  | |  |  |¯¯¯¯¯¯   #
# |  | |  \/  / |  | |    /  /__\  \ \   |   ¯¯¯¯`  | |      |  | |      |  | |  \/  / |  | |   /  /__\  \ \        |  | |      |  | |          |  | |   \______\¯\  #
# |  | |\    / /|  | |   /  /____\  \ \  |  ⌈¯⌈¯¯|  | |      |  | |      |  | |\    / /|  | |  /  /____\  \ \       |  | |       \  \ \____._.  |  | |    _____  | | #
# |__|_| \__/_/ |__|_|  /__/_/    \__\_\ |__|_|  |__|_|      ⌊__⌋_⌋      |__|_| \__/_/ |__|_| /__/_/    \__\_\      ⌊__⌋_⌋         \_______|_|  |__|_|   |______/_/  #
######################################################################################################################################################################
import tomllib
import pygame
import tkinter
win2=tkinter.Tk()

pygame.init()
screen_width = win2.winfo_screenwidth()
screen_height = win2.winfo_screenheight()
win2.destroy()
print(screen_width,screen_height)

file=open('conf.toml','rb')
conf=tomllib.load(file)
file.close()

window=conf['window']
size=window['size']
title=window['title']
icontitle=window['icontitle']
fullscreen=window['fullscreen']
noResolution = window['noResolution']
noWarning = window['noWarning']
icon=pygame.image.load(window['icon'])
fullsize=[None,None]
full=window['fullsize']
if full[0]=='default':
    fullsize[0]=screen_width
else:
    fullsize[0]=full[0]
if full[1]=='default':
    fullsize[1]=screen_height
else:
    fullsize[1]=full[1]

test=conf['test']
test1=test['test1']
test2=test['test2']

game=conf['game']
FPS=game['FPS']
bg=tuple(game['bg'])
vsync=game['vsync']
depth=game['depth']
tick=game['tick']
rectick=game['rectick']
mousespeed=game['mousespeed']
holval=game['holval']
cameraspeed=game['cameraspeed']
seed=game['seed']
randomtickspeed=game['randomtickspeed']
maxelsecount=game['maxelsecount']
pondmaxdis=game['pondmaxdis']
maxpondcount=game['maxpondcount']
maxfriendcount=game['maxfriendcount']
const=game['const']
renderdistance=game['renderdistance']
renderdistance2=renderdistance
def ch(sc):
    global renderdistance
    renderdistance=sc*renderdistance2
renderdistancetoscreen=game['renderdistancetoscreen']


message=conf['message']
deathmessage=message['deathmessage']
pausemessage=message['pausemessage']
waitmessage=message['waitmessage']

senior=conf['senior']
blocksize=senior['blocksize']