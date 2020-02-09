
## TRex-Game.py
## Software Requirements:
# ncurses library
# Python 2.7
## Syntax:
# > py -2.7 TRex-Game.py

import curses
from time import sleep
from Scene import Ground,Cloud,Cactus
from Actors import Trex

BORDER_X,BORDER_Y = 100,30
PAD_X,PAD_Y = 2,2
NO_BORDER = 0
HORIZON = (BORDER_Y//2)
HORIZON_1BY3 = (BORDER_Y//3)
HORIZON_2BY3 = (2*BORDER_Y//3)

#score board
SCORE_X,SCORE_Y = 85,3
SCORE_BOARD_HEADER = "The T-REX Game"
SCORE_TITLE = "SCORE: "
LEVEL_TITLE = "LEVEL: "
# delays
SHORT_DELAY = (30000/1000000.0)
DELAY = (50000/1000000.0)
LONG_DELAY = (60000/1000000.0)

# key codes
KEY_SPACEBAR = 32
KEY_ESC = 27
KEY_ENTER =10
KEY_NONE = 0

# misc
MAX_JUMP = 5


# game states
GS_INIT = 1
GS_START = 2
GS_RUN = 3
GS_COLLISION = 4
GS_EXIT = 0
GS_ERROR = -1


class TRexGame:
    def __init__(self,window):
        # init objects
        self.window = window
        self.ground = Ground(window)
        self.cloud = Cloud(window)
        self.trex = Trex(window)
        self.score = 0

    def draw_score(self):
        self.window.addstr(SCORE_Y-2,SCORE_X-3,SCORE_BOARD_HEADER)
        self.window.addstr(SCORE_Y,SCORE_X,SCORE_TITLE + str(self.score))
        self.window.addstr(SCORE_Y+1,SCORE_X, LEVEL_TITLE + str(self.score//100))

    def check_collision(self):
        trex_pos = self.trex.get_trex_range()
        cactus_pos = self.ground.get_cactus_pos()

        trex_y,trex_x = trex_pos[0],trex_pos[1]
        cactus_y,cactus_x = cactus_pos[0],cactus_pos[1]

        if (abs(cactus_x-trex_x)<3) and (abs(cactus_y-trex_y)<2):
            return True

    def update_all(self):
        self.score += 1
        speed = self.score//200+3
        self.ground.update(speed)
        self.cloud.update()
        self.trex.update()
        if self.check_collision():
            self.trex.die()

    def draw_all(self):
        window.clear()
        self.cloud.draw()
        self.ground.draw()
        self.trex.draw()
        self.draw_score()

    def handle_controls(self):
        if window.getch() is KEY_SPACEBAR:
            self.trex.jump()

    def is_end_of_game(self):
        return self.check_collision()

    def start(self, window):
        while(not self.is_end_of_game()):
            self.handle_controls()
            self.update_all()
            self.draw_all()
            sleep(0.06)
        sleep(2)

    def draw_at(self, y, x, image):
        for i, line in enumerate(image):
            self.window.addstr(y+i, x, line)

    def should_continue(self):
        self.window.clear()
        self.window.border(NO_BORDER)
        self.draw_at(10, 27, [
            "  ___   _   __  __ ___    _____   _____ ___ ",
            " / __| /_\ |  \/  | __|  / _ \ \ / / __| _ \\",
            "| (_ |/ _ \| |\/| | _|  | (_) \ V /| _||   /",
            " \___/_/ \_\_|  |_|___|  \___/ \_/ |___|_|_\\",
            "",
            "             FINAL_SCORE : "+str(self.score),
            "",
            "Press 'Enter' Key to Restart or 'ESC' to Quit"
        ])
        while(True):
            key_event = self.window.getch()
            if key_event is KEY_ESC:
                return False
            elif key_event is KEY_ENTER:
                return True


if __name__ == '__main__':

    # prepare game environment
    curses_lib = curses.initscr()
    window = curses.newwin(BORDER_Y,BORDER_X,0,0)
    curses.noecho()
    curses.curs_set(0)
    window.border(NO_BORDER)
    window.nodelay(1)

    while(True):
        main_game = TRexGame(window)
        main_game.start(window)
        if not main_game.should_continue():
            break

    # clean up
    window.clear()
    window.refresh()
    curses.endwin()

