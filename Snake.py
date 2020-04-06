import time
import random
from sense_hat import SenseHat
from settings import *


class Snake_game:

    def __init__(self):
        self.sense = SenseHat()
        self.trail = [[3, 3]]
        self.direction = [1, 0]  # x y
        self.length = 1
        self.apple_pos = [random.randint(0, 7), random.randint(0, 7)]
        self.pixels = [clear] * 64

    # 0 = up, 1 = right, 2 = down, 3 = left
    def set_direction(self, dir):
        if dir == 0:
            self.direction = [0, -1]
        elif dir == 1:
            self.direction = [1, 0]
        elif dir == 2:
            self.direction = [0, 1]
        elif dir == 3:
            self.direction = [-1, 0]

    # game loop
    def play_game(self):

        while True:
            self.pixels = [clear] * 64

            # sense HAT controller
            for event in self.sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "up":
                        self.set_direction(0)
                    elif event.direction == "right":
                        self.set_direction(1)
                    elif event.direction == "down":
                        self.set_direction(2)
                    elif event.direction == "left":
                        self.set_direction(3)

            self.trail.insert(0, [self.trail[0][0] + self.direction[0], self.trail[0][1] + self.direction[1]])

            # one border cross in and the other off
            if self.trail[0][0] < 0:
                self.trail[0][0] = 7
            if self.trail[0][1] < 0:
                self.trail[0][1] = 7
            if self.trail[0][0] > 7:
                self.trail[0][0] = 0
            if self.trail[0][1] > 7:
                self.trail[0][1] = 0

            if self.trail[0] == self.apple_pos:
                self.apple_pos = []
                while self.apple_pos == []:
                    self.apple_pos = [random.randint(0, 7), random.randint(0, 7)]
                    if self.apple_pos in self.trail:
                        self.apple_pos = []
                self.length += 1
            # snake runs into itself
            elif self.trail[0] in self.trail[1:]:
                self.length = 1
            else:
                while len(self.trail) > self.length:
                    self.trail.pop()

            for pos in self.trail:
                self.pixels[pos[1] * 8 + pos[0]] = white

            # y * rowSize + x
            self.pixels[self.apple_pos[1] * 8 + self.apple_pos[0]] = red
            # apple position (red led)
            self.sense.set_pixels(self.pixels)

            time.sleep(0.15)
