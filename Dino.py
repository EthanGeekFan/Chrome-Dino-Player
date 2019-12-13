import pyautogui as gui
import threading
from mss import mss


mon = {'top': 175, 'left': 513, 'width': 507, 'height': 89}
H_BIRD = (49, 39)
M_BIRD = (74, 64)
OBSTACLE_DAY = (83, 83, 83)
OBSTACLE_NIGHT = (172, 172, 172)
WHITE = (255, 255, 255)


def big_jump():
    gui.keyDown('up')
    gui.sleep(0.1)
    gui.keyUp('up')


def small_jump():
    gui.press('up')
    gui.sleep(0.1)
    gui.press('down')


def duck(sec):
    gui.keyDown('down')
    gui.sleep(sec)
    gui.keyUp('down')



def detect(pic):
    count = 0
    threadLock.acquire()
    img = pic
    threadLock.release()
    bird = 3
    w, h = len(img[0]), len(img)
    x_min = w
    x_max = 0
    y_min = 0
    y_max = h
    x_n_min = w
    x_n_max = 0
    y_n_min = 0
    y_n_max = h
    for x in range(w):
        for y in range(h):
            if img[y][x] == OBSTACLE_DAY or img[y][x] == OBSTACLE_NIGHT:
                if -30 < x - x_min < 0 or x_min == w:
                    x_min = x
                if 30 > x - x_max > 0 or x_max == 0:
                    x_max = x
                if 25 > y - y_min > 0 or y_min == 0:
                    y_min = y
                if -25 < y - y_max < 0 or y_max == h:
                    y_max = y
                if x - x_max > 30:
                    if -30 < x - x_n_min < 0 or x_n_min == w:
                        x_n_min = x
                    if 30 > x - x_n_max > 0 or x_n_max == 0:
                        x_n_max = x
                    if 25 > y - y_n_min > 0 or y_n_min == 0:
                        y_n_min = y
                    if -25 < y - y_n_max < 0 or y_n_max == h:
                        y_n_max = y
    if H_BIRD[0] >= y_min >= H_BIRD[1]:
        bird = 0
    elif M_BIRD[0] >= y_min >= M_BIRD[1]:
        bird = 1
    if x_min < x_max and 30 < x_min < 80:
        if bird == 3:
            if x_max - x_min < 30:
                small_jump()
            else:
                big_jump()
        elif bird == 1:
            duck(0.5)


class Eye(threading.Thread):

    def __init__(self, brain):
        threading.Thread.__init__(self)
        self.name = 'Eye'
        self.brain = brain

    def run(self):
        with mss() as sct:
            print('Eyes opened! ')
            while True:
                cache = sct.grab(mon).pixels
                if not threadLock.locked():
                    self.brain.img = cache


class Brain:

    def __init__(self):
        self.img = None
        self.eye = Eye(self)
        # self.clock = Clock(self)

    def start(self):
        self.eye.start()
        # self.clock.start()
        while True:
            if self.img is not None:
                detect(self.img)


class Clock(threading.Thread):

    def __init__(self, brain):
        threading.Thread.__init__(self)
        self.name = 'Clock'
        self.brain = brain

    def check_day(self, img):
        pix = []
        for row in img:
            for col in row:
                pix.append(col)
        if not set(pix).__contains__(WHITE) and self.OBSTACLE != (172, 172, 172):
            self.OBSTACLE = (172, 172, 172)
            print('Night! ')
        elif set(pix).__contains__(WHITE) and self.OBSTACLE != (83, 83, 83):
            self.OBSTACLE = (83, 83, 83)
            print('Day!')

    def run(self):
        while True:
            if self.brain.img is not None:
                self.check_day(self.brain.img)


threadLock = threading.Lock()
brain = Brain()
brain.start()


