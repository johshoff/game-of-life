#!/usr/bin/env python3
import time
import sys
from random import random

def amod(a, b):
    '''Awesome mod; a non-negative modulus, unlike the % operator.'''
    return ((a % b) + b) % b

class Board:
    def __init__(self, w, h):
        self.nodes = [' ' for _ in range(w * h)]
        self.width = w
        self.height = h

    def get(self, x, y):
        x = amod(x, self.width)
        y = amod(y, self.height)
        return self.nodes[x + y * self.width]

    def set(self, node, x, y):
        self.nodes[x + y * self.width] = node
    
    def set_pattern(self, pattern, x, y):
        for dx, node in enumerate(pattern):
            self.set(node, x + dx, y)
    
    def set_glider(self, x, y):
        self.set_pattern(' x ', x, y)
        self.set_pattern('  x', x, y + 1)
        self.set_pattern('xxx', x, y + 2)
    
    def neighbors(self, x, y):
        n = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if self.get(x + dx, y + dy) == 'x':
                    n += 1
        return n
    
    def iterate(self):
        new_board = Board(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                n = self.neighbors(x, y)
                if self.get(x, y) == 'x':
                    if n == 2 or n == 3:
                        new_board.set('x', x, y)
                else:
                    if n == 3:
                        new_board.set('x', x, y)
        self.nodes = new_board.nodes

    def randomize(self, fill_rate):
        for y in range(self.height):
            for x in range(self.width):
                is_set = random() < fill_rate
                self.set('x' if is_set else ' ', x, y)
    
    def __str__(self):
        ret = ''
        for y in range(0, self.height, 2):
            for x in range(self.width):
                upper = self.get(x, y) == 'x'
                lower = self.get(x, y + 1) == 'x'
                ret += '█' if upper and lower else ('▀' if upper else ('▄' if lower else ' '))
            ret += '\n'
        return ret[:-1]
        
width  = int(sys.argv[1]) if len(sys.argv) >= 2 else 80
height = int(sys.argv[2]) if len(sys.argv) >= 3 else 80
b = Board(width, height)
b.randomize(0.3)
# clear screen and hide cursor
print('\033[2J\033[?25l')
try:
    while True:
        # move to top left corner
        print('\033[H', end='')
        print(b)
        b.iterate()
        time.sleep(1/60)
except KeyboardInterrupt:
    # clear screen and restore cursor
    print('\033[2J\033[H\033[?25h', end='')
