# Actors.py

TREX_SPRITES = [
    [ # stride
        "   =o===",
        "   ==www",
        ", |||-",
        "\||||",
        "  / \\",
    ],
    [ # legs closed
        "   =o===",
        "   ==www",
        ", |||-",
        "\||||",
        "  \ /"
    ],
    [ # jumping
        "   =-===",
        "   ==www",
        ", |||-",
        "\||||",
        "  L L"
    ],
    [ # dead
        "   =X===",
        "   ==www",
        ", |||-",
        "\||||",
        "  L L"
    ]
]


class Trex:
    def __init__(self,draw_at,):
        self.draw_at = draw_at
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
        return [self.y,(self.x + 4)]

    def image(self):
        if self.dead:
            return TREX_SPRITES[3]
        elif self.jump_state:
            return TREX_SPRITES[2]
        return TREX_SPRITES[self.frame//2]

    def draw(self):
        self.draw_at(self.y-4, self.x, self.image())

    def update(self):
        self.frame = (self.frame + 1) % 4
        if self.jump_state:
            jmp = [-1,-2,-3,0, 0,1,2,3]
            self.y = self.y + jmp[self.count]
            self.count = (self.count + 1)%len(jmp)
            if self.y >= 20:
                self.y = 20
                self.jump_state = False
