# Actors.py

TREX = [
    "   =o===",
    "   ==www",
    ", |||-",
    "\||||",
    "  / \\",
    "  / \\",
    "  \ /",
    "  \ /"
]
TREX_DEAD_0 = "   =X==="
TREX_JUMP_4 = "  L L"


class Trex:
    def __init__(self,window,):
        self.window = window
        self.image = []
        self.jump_state = False
        self.y = 20
        self.x = 4
        self.count = 0
        self.dead = False
        self.frame = 0

    def jump(self):
        self.jump_state = True

    def die(self):
        self.dead = True

    def get_trex_range(self):
        return [self.y,(self.x + 6)]

    def draw(self):
        self.image = TREX[:5]
        if self.dead:
            self.image[0] = TREX_DEAD_0
        if not self.jump_state:
            self.image[4] = TREX[4 + self.frame]
        else:
            self.image[4] = TREX_JUMP_4

        self.window.addstr(self.y-4,self.x,self.image[0])
        self.window.addstr(self.y-3,self.x,self.image[1])
        self.window.addstr(self.y-2,self.x,self.image[2])
        self.window.addstr(self.y-1,self.x,self.image[3])
        self.window.addstr(self.y ,self.x,self.image[4])

    def update(self):
        self.frame = (self.frame + 1) % 4
        if self.jump_state:
            jmp = [-1,-2,-3,0, 0,1,2,3]
            self.y = self.y + jmp[self.count]
            self.count = (self.count + 1)%len(jmp)
            if self.y >= 20:
                self.y = 20
                self.jump_state = False
