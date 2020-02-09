# Scene.py
from random import randint
import curses

ground = "___________________&______.._______________;.,,,_____________________&______.._____________________"

ground_type = ["________","_&______","__;_____","........"]
GROUND_FLAT = 0
GROUND_GRASS = 1
GROUND_ROCK = 2
GROUND_BROKEN = 3
NUM_GND = 4
G_Y,G_X = 20,2

CACTI_LEVEL_0 = ["   ","# |  ","#_|_#","  |  "]
CACTI_LEVEL_1 = ["   ","#_| #","|_#  ","  |  "]
CACTI_LEVEL_2 = ["# | #","#_| #","|_#  ","  |  "]
CACTI_LEVEL_3 = ["# | #","# |_#","#_|  ","  |  "]
CACTI_LEVEL_4 = ["# |  ","# | #","#_|_#","  |  "]

CACTI_OFFSET = 96

class Cloud:
    def __init__(self,window):
        self.window = window
        self.clouds = []

    def draw(self):
        for pos in self.clouds:
            self.window.addstr(pos[0], pos[1],"   @@@", curses.A_DIM)
            self.window.addstr(pos[0]+1, pos[1],"..@@@@@....", curses.A_DIM)

    def update(self):
        if randint(1, 30) == 1 or len(self.clouds) < 1:
            self.clouds.append((randint(5,10), 90))
        self.clouds = [(c[0], c[1]-1) for c in self.clouds if c[1]>2]

class Cactus:
    def __init__(self,window):
        self.window = window
        self.x = 96
        c = [CACTI_LEVEL_0,CACTI_LEVEL_1,CACTI_LEVEL_2,CACTI_LEVEL_3,CACTI_LEVEL_4]
        self.image = c[randint(0,2)]

    def draw(self,y):
        self.window.addstr(y-3,self.x,   self.image[0])
        self.window.addstr(y-2,self.x,   self.image[1])
        self.window.addstr(y-1,self.x,   self.image[2])
        self.window.addstr(y,self.x,     self.image[3])

    def update(self,y,image, speed):
        self.x -= speed

class Ground:
    def __init__(self,window):
        self.ground = ground
        self.window = window
        self.cactus = Cactus(self.window)

    def draw(self):
        self.window.addstr(G_Y, G_X, self.ground)
        self.cactus.draw(G_Y)

    def get_cactus_pos(self):
        return [20, self.cactus.x]

    def update(self,speed):
        # prepare ground using random ground types
        # these ground type have visual value and
        # donot change the gameplay in any way
        image = ""
        gtype_idx = int(randint(0,NUM_GND)%NUM_GND)
        image = self.ground + ground_type[gtype_idx]
        self.ground = image[speed:speed+94]
        # draw the initial ground

        self.cactus.update(20,image, speed)
        if self.cactus.x < speed:
            self.cactus = Cactus(self.window)


