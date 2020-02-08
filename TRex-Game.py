
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
        self.level = 1
        self.cactus_pos = [-1,-1]

        # init objects
        self.window = window
        self.ground = Ground(window)
        self.cloud = Cloud(window)
        self.cacti = Cactus(window)
        self.trex = Trex(window)


    def draw_score(self, score):
        self.window.addstr(SCORE_Y-2,SCORE_X-3,SCORE_BOARD_HEADER)
        self.window.addstr(SCORE_Y,SCORE_X,SCORE_TITLE + str(score))
        self.window.addstr(SCORE_Y+1,SCORE_X, LEVEL_TITLE + str(self.level))

    def level_up(self, score):
        if (score%100 == 0) and score > 0:
            self.level = self.level + 1
            curses.beep()


    def check_collision(self):
        trex_pos = self.trex.get_trex_range()
        if self.cactus_pos is None:
            return

        trex_y,trex_x = trex_pos[0],trex_pos[1]
        cactus_y,cactus_x = self.cactus_pos[0],self.cactus_pos[1]

        if (cactus_x <= 16 and cactus_x >= 11) and (abs(cactus_y - trex_y) < 2):
            return True


    def start(self, window):
        score = 0
        while(True):
            window.clear()
            window.border(NO_BORDER)
            self.draw_score(score)
            self.cloud.update()

            self.cactus_pos = self.ground.update(self.level)
            self.trex.update()
            isCollision = self.check_collision()
            if isCollision:
                self.trex.die()
            self.trex.draw()
            if window.getch() is KEY_SPACEBAR:
                self.trex.jump()
            score += 1
            self.level_up(score)
            if isCollision:
                sleep(2)
                break
            sleep(0.1)
        return score


def should_continue(window, score):
    window.clear()
    window.border(NO_BORDER)
    window.addstr(10, 27, "  ___   _   __  __ ___    _____   _____ ___ ")
    window.addstr(11, 27, " / __| /_\ |  \/  | __|  / _ \ \ / / __| _ \\")
    window.addstr(12, 27, "| (_ |/ _ \| |\/| | _|  | (_) \ V /| _||   /")
    window.addstr(13, 27, " \___/_/ \_\_|  |_|___|  \___/ \_/ |___|_|_\\")
    window.addstr(15, 27, "             FINAL_SCORE : "+str(score))
    window.addstr(17, 27, "Press 'Enter' Key to Restart or 'ESC' to Quit")
    while(True):
        key_event = window.getch()
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
        score = main_game.start(window)
        if not should_continue(window, score):
            break

    # clean up
    window.clear()
    window.refresh()
    curses.endwin()

