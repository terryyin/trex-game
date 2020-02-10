from random import randint
import curses
from sprites import TREX_SPRITES, GROUND_SPRITE, CACTUS_SPRITES, CLOUD_SPRITE

GND_Y = 20
CACTUS_START_X = 96

def draw_at(window, y, x, image, dim=False):
    for i, line in enumerate(image):
        window.addstr(y+i, x, line, 0 if dim else curses.A_DIM)

class Trex:
    def __init__(self, window):
        self.window = window
        self.jumping = None
        self.jump_state = 0
        self.y = GND_Y
        self.x = 4
        self.dead = False
        self.frame = 0

    def jump(self):
        self.jumping = True

    def die(self):
        self.dead = True

    def check_collision(self, object_pos):
        if (abs(object_pos[1]-self.x-4)<3) and (abs(object_pos[0]-self.y)<2):
            return True
        return False

    def get_image(self):
        if self.dead:
            return TREX_SPRITES[3]
        elif self.jumping:
            return TREX_SPRITES[2]
        return TREX_SPRITES[self.frame]

    def draw(self):
        draw_at(self.window, self.y-4, self.x, self.get_image())

    def update(self):
        self.frame = (self.frame + 1) % 2
        if self.jumping:
            jmp = [-3,-2,-1,0, 0,1,2,3]
            self.y = self.y + jmp[self.jump_state]
            self.jump_state += 1
            if self.y >= GND_Y:
                self.y = GND_Y
                self.jumping = False
                self.jump_state = 0


class Cloud:
    def __init__(self,window):
        self.window = window
        self.clouds = []

    def draw(self):
        for pos in self.clouds:
            draw_at(self.window, pos[0], pos[1], CLOUD_SPRITE, True)

    def update(self):
        if randint(1, 30) == 1 or len(self.clouds) < 1:
            self.clouds.append((randint(5,10), 90))
        self.clouds = [(c[0], c[1]-1) for c in self.clouds if c[1]>2]


class Cactus:
    def __init__(self):
        self.x = CACTUS_START_X
        sprite_index = randint(0,len(CACTUS_SPRITES)-1)
        self.image = CACTUS_SPRITES[sprite_index]

    def update(self, speed):
        self.x -= speed

    def draw(self, window):
        draw_at(window, GND_Y-3, self.x, self.image)


class Cacti:
    def __init__(self,window):
        self.window = window
        self.cacti = []

    def draw(self):
        for cactus in self.cacti:
            cactus.draw(self.window)

    def _enough_space_from_the_last_cactus(self, speed):
        if len(self.cacti) < 1:
            return True
        if self.cacti[-1].x < CACTUS_START_X - 9*speed:
            return True
        return False

    def update(self, speed):
        for cactus in self.cacti:
            cactus.update(speed)
        while(self.cacti and self.cacti[0].x < speed):
            self.cacti.pop(0)
        if self._enough_space_from_the_last_cactus(speed):
            if randint(0, 10) == 0:
                self.cacti.append(Cactus())

    def get_first_pos(self):
        if self.cacti:
            return [GND_Y, self.cacti[0].x]
        return [GND_Y, 100]


class Ground:
    def __init__(self,window):
        self.image = GROUND_SPRITE
        self.window = window

    def draw(self):
        draw_at(self.window, GND_Y, 2, [self.image])

    def update(self,speed):
        self.image = self.image[speed:speed+94] + self.image[:speed]
