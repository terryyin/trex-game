import curses
from time import sleep
from GameObjects import Trex, Ground, Cloud, Cacti, draw_at

# key codes
KEY_SPACEBAR = 32
KEY_ESC = 27
KEY_ENTER =10

class TRexGame:
    def __init__(self,window):
        self.window = window
        self.ground = Ground(window)
        self.cacti = Cacti(window)
        self.cloud = Cloud(window)
        self.trex = Trex(window)
        self.score = 0

    def draw_score(self):
        draw_at(window, 1, 82, [
            "The T-REX Game",
            "",
            "   SCORE: " + str(self.score),
            "   LEVEL: " + str(self.score//100)
        ])

    def check_collision(self):
        trex_pos = self.trex.get_pos()
        cactus_pos = self.cacti.get_first_pos()

        trex_y,trex_x = trex_pos[0],trex_pos[1]
        cactus_y,cactus_x = cactus_pos[0],cactus_pos[1]

        if (abs(cactus_x-trex_x)<3) and (abs(cactus_y-trex_y)<2):
            return True

    def update_all(self):
        self.score += 1
        speed = self.score//200+3
        self.ground.update(speed)
        self.cacti.update(speed)
        self.cloud.update()
        self.trex.update()
        if self.check_collision():
            self.trex.die()

    def draw_all(self):
        window.clear()
        self.cloud.draw()
        self.ground.draw()
        self.cacti.draw()
        self.trex.draw()
        self.draw_score()
        window.refresh()

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

    def should_continue(self):
        self.window.clear()
        self.window.border(0)
        draw_at(window, 10, 27, [
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
    window = curses.newwin(30,100,0,0)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
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

