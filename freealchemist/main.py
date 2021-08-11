#!/usr/bin/python
"""
Copyright (C) 2008-2021 Davide Gessa

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02111-1301  USA
"""

import random
import sys
import time
import os
from pygame.locals import *
import pygame

__author__ = "Davide Gessa"
__email__ = "dak.linux@gmail.com"
__program__ = "FreeAlchemist"
__version__ = "0.7"
__copyright__ = "Copyright (c) 2008-2021 Davide Gessa"
__license__ = "GPL"
__sleep__ = 0.1


width = 6
size_x = 10
size_y = 8

def abpath(f):
    return os.path.abspath(os.path.dirname(__file__)) + "/" + f


class FreeAlchemist:
    def __init__(self):
        self.grid = []
        self.nextblock = []
        self.blockgrid = []
        self.blockpos = None
        self.points = None
        self.lim = None
        self.totalpoints = 0
        self.mov = None
        self.over = None
        self.fail = None
        self.time = None

        # Per quanto riguarda pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((446, 435))
        pygame.display.set_caption(__program__+" "+__version__)
        pygame.mouse.set_visible(0)

        self.font = pygame.font.Font(None, 24)
        self.background = pygame.image.load(abpath("media/background.png")).convert()
        self.gameover = pygame.image.load(abpath("media/gameover.png"))
        self.p = [None]*16
        self.p[0] = pygame.image.load(abpath("media/p1.png"))  # 20
        self.p[1] = pygame.image.load(abpath("media/p2.png"))  # 40
        self.p[2] = pygame.image.load(abpath("media/p3.png"))  # 70
        self.p[3] = pygame.image.load(abpath("media/p4.png"))  # 110
        self.p[4] = pygame.image.load(abpath("media/p5.png"))  # 150
        self.p[5] = pygame.image.load(abpath("media/p6.png"))  # 200
        self.p[6] = pygame.image.load(abpath("media/p7.png"))  # 260
        self.p[7] = pygame.image.load(abpath("media/p8.png"))  # 330
        self.p[8] = pygame.image.load(abpath("media/p9.png"))  # 410
        self.p[9] = pygame.image.load(abpath("media/p10.png"))  # 500
        self.p[10] = pygame.image.load(abpath("media/p11.png"))  # 600
        self.p[11] = pygame.image.load(abpath("media/p12.png"))  # 1000
        self.p[13] = pygame.image.load(abpath("media/p14.png"))
        self.p[14] = pygame.image.load(abpath("media/p15.png"))
        self.p[15] = pygame.image.load(abpath("media/p16.png"))

        self.s = [None]*5
        #self.s[0] = pygame.mixer.Sound("explode.wav")

    def newGame(self):
        print("[*] New Game")

        self.lim = 3
        self.over = False
        self.mov = False
        self.fail = 0
        self.time = 0.0

        # Svuota i punti
        self.points = 0

        # Riempie la griglia
        self.grid = []

        for x in range(size_x):
            line = []
            for y in range(size_y):
                line.append(0)
            self.grid.append(line)

        # Riempie la box dei block
        self.blockgrid = []
        self.nextblock = [
            [random.randint(1, self.lim), random.randint(1, self.lim)], [0, 0]]
        self.blockpos = 0

        for x in range(2):
            line = [0, 0]
            self.blockgrid.append(line)

    def genBlock(self):
        self.unBorder()
        self.blockgrid = self.nextblock

        if random.randint(1, 30) == 25:
            self.nextblock = [
                [random.randint(14, 16), random.randint(1, self.lim)], [0, 0]]
        else:
            self.nextblock = [
                [random.randint(1, self.lim), random.randint(1, self.lim)], [0, 0]]

    def onBoard(self, x, y):
        return x >= 0 and x < len(self.grid) and y >= 0 and y < len(self.grid[0])

    def test(self, x, y, dx1, dy1, dx2, dy2, t):
        return self.onBoard(x+dx1, y+dy1) and self.onBoard(x+dx2, y+dy2) and self.grid[x+dx1][y+dy1] == t and self.grid[x+dx2][y+dy2] == t

    def updateGame(self):
        # Controlla se ci son spazi vuoti da riempire
        md = False
        for x in range(len(self.grid)-1, -1, -1):
            for y in range(0, len(self.grid[0])):
                s = 0
                for a in range(len(self.grid)):
                    s += self.grid[a][y]

                if self.grid[x][y] == 0 and s > 0:
                    for a in range(x, 0, -1):
                        if self.grid[a-1][y] != 0:
                            self.grid[a][y] = self.grid[a-1][y]
                            self.grid[a-1][y] = 0
                            md = True
        self.mov = md

        # Controlliamo se possiamo far esplodere qualcosa :P
        if not self.mov:
            for x in range(0, len(self.grid)):
                for y in range(0, len(self.grid[0])):
                    # La pressa
                    if self.grid[x][y] == 15 and x == len(self.grid)-2:
                        self.grid[len(self.grid)-2][y] = 0
                        self.grid[len(self.grid)-1][y] = 0

                    elif self.grid[x][y] == 15:
                        if x < len(self.grid)-1:
                            self.grid[x][y] = 0
                            self.grid[x+1][y] = 15

                    # Bomba 1
                    elif self.grid[x][y] == 14:
                        self.grid[x][y] = 0
                        if self.onBoard(x, y-1):
                            self.grid[x][y-1] = 0
                        if self.onBoard(x, y+1):
                            self.grid[x][y+1] = 0
                        if self.onBoard(x+1, y):
                            self.grid[x+1][y] = 0
                        if self.onBoard(x-1, y):
                            self.grid[x-1][y] = 0

                    # Bomba 2
                    elif self.grid[x][y] == 16:
                        self.grid[x][y] = 0
                        if self.onBoard(x, y-1):
                            self.grid[x][y-1] = 0
                        if self.onBoard(x, y+1):
                            self.grid[x][y+1] = 0
                        if self.onBoard(x+1, y):
                            self.grid[x+1][y] = 0
                        if self.onBoard(x-1, y):
                            self.grid[x-1][y] = 0
                        if self.onBoard(x-1, y-1):
                            self.grid[x-1][y-1] = 0
                        if self.onBoard(x+1, y+1):
                            self.grid[x+1][y+1] = 0
                        if self.onBoard(x+1, y-1):
                            self.grid[x+1][y-1] = 0
                        if self.onBoard(x-1, y+1):
                            self.grid[x-1][y+1] = 0
                        if self.onBoard(x, y-2):
                            self.grid[x][y-2] = 0
                        if self.onBoard(x, y+2):
                            self.grid[x][y+2] = 0
                        if self.onBoard(x+2, y):
                            self.grid[x+2][y] = 0
                        if self.onBoard(x-2, y):
                            self.grid[x-2][y] = 0

                    # Normale
                    elif self.grid[x][y] != 0 and self.grid[x][y] < 13:
                        t = self.grid[x][y]
                        if self.test(x, y, 0, 1, 0, -1, t) or self.test(x, y, 1, 0, -1, 0, t) or self.test(x, y, 1, 0, 0, 1, t) or self.test(x, y, -1, 0, 0, -1, t) or self.test(x, y, -1, 0, 0, 1, t) or self.test(x, y, 1, 0, 0, -1, t):
                            # upgrade our center piece
                            if t < 12:
                                self.grid[x][y] += 1
                            else:
                                self.grid[x][y] = 0
                            # explode the touching pieces
                            self.explode(x, y, t)
                            self.points += (t*10)+t*t

                        if t-1 > self.lim and t-1 < 13:
                            self.lim += 1

        if self.points % 2 != 0:
            self.points += 1

        # Se ci son cubetti nelle prime due righe, game over
        if not self.mov:
            if sum(self.grid[0]) > 0:
                self.fail += 1
            elif sum(self.grid[1]) > 0:
                self.fail += 1
            else:
                self.fail = 0
        if self.fail > 2:
            self.over = True

    # Explode the piece at position x,y if type == t
    # and also explode all touching pieces of the same type.
    def explode(self, x, y, t):
        if self.grid[x][y] == t:
            self.grid[x][y] = 0
        # recursively explode touching pieces of the same type
        if (y > 0):
            if self.grid[x][y-1] == t:
                self.explode(x, y-1, t)
        if (y < len(self.grid[0])-1):
            if self.grid[x][y+1] == t:
                self.explode(x, y+1, t)
        if (x > 0):
            if self.grid[x-1][y] == t:
                self.explode(x-1, y, t)
        if (x < len(self.grid)-1):
            if self.grid[x+1][y] == t:
                self.explode(x+1, y, t)

    def renderGame(self):
        self.screen.fill([0, 0, 0])
        self.screen.blit(self.background, (0, 0))

        # Renderizza il punteggio
        text = self.font.render(str(self.points), 1, (255, 255, 255))
        self.screen.blit(text, (15, 50))

        text = self.font.render(
            ("%.2f min" % (self.time/60.)), 1, (255, 255, 255))
        self.screen.blit(text, (15, 25))

        # Renderizza i nexblock
        self.screen.blit(self.p[self.nextblock[0][0]-1], ((10), (77)))
        self.screen.blit(self.p[self.nextblock[0][1]-1], ((46), (77)))

        # Renderizza i block correnti
        if self.blockgrid[0][0] != -1:
            if self.blockgrid[0][0] != 0:
                self.screen.blit(
                    self.p[self.blockgrid[0][0]-1], ((106+40*self.blockpos), (7)))
            if self.blockgrid[0][1] != 0:
                self.screen.blit(
                    self.p[self.blockgrid[0][1]-1], ((106+40+40*self.blockpos), (7)))
            if self.blockgrid[1][0] != 0:
                self.screen.blit(
                    self.p[self.blockgrid[1][0]-1], ((106+40*self.blockpos), (7+40)))
            if self.blockgrid[1][1] != 0:
                self.screen.blit(
                    self.p[self.blockgrid[1][1]-1], ((106+40+40*self.blockpos), (7+40)))

        # Renderizza tutta la griglia
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] != 0:
                    self.screen.blit(
                        self.p[self.grid[x][y]-1], ((106+y*40), (25+x*40)))

        pygame.display.update()
        # pygame.time.delay(100)

    def exitGame(self):
        print("[*] Exit")
        sys.exit()

    def goLeft(self):
        # the left pieces of the square blockpos
        left_part = [self.blockgrid[0][0], self.blockgrid[1][0]]
        if self.blockpos > 0:
            self.blockpos -= 1
        # if we are on the extreme left, we still can go further
        # at least if our pieces are vertical
        elif self.blockpos == 0 and left_part == [0, 0]:
            self.blockpos -= 1

    def goRight(self):
        # the right pieces of the square blockpos
        right_part = [self.blockgrid[0][1], self.blockgrid[1][1]]
        if self.blockpos < width:
            self.blockpos += 1
        # if we are on the extreme right, we still can go further
        # at least if our pieces are vertical
        elif self.blockpos == width and right_part == [0, 0]:
            self.blockpos += 1

    def unBorder(self):
        if self.blockpos == width+1:
            self.goLeft()
        if self.blockpos == -1:
            self.goRight()

    def keyInputs(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exitGame()

            elif event.type == KEYDOWN:
                if not self.mov:
                    if event.key == K_UP:
                        self.unBorder()
                        old = self.blockgrid[0] + self.blockgrid[1]
                        self.blockgrid = [[old[2], old[0]], [old[3], old[1]]]

                    elif event.key == K_DOWN:
                        self.unBorder()
                        old = self.blockgrid[0] + self.blockgrid[1]
                        self.blockgrid = [[old[1], old[3]], [old[0], old[2]]]

                    elif event.key == K_RIGHT:
                        self.goRight()

                    elif event.key == K_LEFT:
                        self.goLeft()

                    elif event.key == K_SPACE:
                        self.mov = True
                        self.points += 10
                        # We set only the non zero pieces
                        if self.blockgrid[0][0] != 0:
                            self.grid[0][self.blockpos] = self.blockgrid[0][0]
                        if self.blockgrid[0][1] != 0:
                            self.grid[0][self.blockpos +
                                         1] = self.blockgrid[0][1]
                        if self.blockgrid[1][0] != 0:
                            self.grid[1][self.blockpos] = self.blockgrid[1][0]
                        if self.blockgrid[1][1] != 0:
                            self.grid[1][self.blockpos +
                                         1] = self.blockgrid[1][1]
                        self.blockgrid[0][0] = -1

                if event.key == K_PAUSE or event.key == K_ESCAPE or event.key == K_p:
                    print("[*] Pause")
                    pause = 1

                    self.screen.blit(self.gameover, (0, 0))
                    self.screen.blit(pygame.font.Font(None, 36).render(
                        "Pause", 1, (255, 255, 255)), (20, 20))
                    self.screen.blit(pygame.font.Font(None, 24).render(
                        "Press any key", 1, (255, 255, 255)), (416-120, 400-20))
                    pygame.display.update()

                    while pause:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                self.exitGame()

                            elif event.type == KEYDOWN:
                                pause = 0
                        time.sleep(__sleep__)

    def start(self):
        # Presentazione iniziale
        intro = 0
        print("[*] FreeAlchemist")

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.gameover, (0, 0))
        self.screen.blit(pygame.font.Font(None, 36).render(
            __program__+" "+__version__, 1, (255, 255, 255)), (20, 20))

        self.screen.blit(self.p[0], (40, 50))
        self.screen.blit(self.p[1], (88, 50))
        self.screen.blit(self.p[2], (88+48, 50))
        self.screen.blit(self.p[3], (88+88, 50))
        self.screen.blit(self.p[4], (88*2+48, 50))
        self.screen.blit(self.p[5], (88*3, 50))
        self.screen.blit(self.p[6], (40, 100))
        self.screen.blit(self.p[7], (88, 100))
        self.screen.blit(self.p[8], (88+48, 100))
        self.screen.blit(self.p[9], (88+88, 100))
        self.screen.blit(self.p[10], (88*2+48, 100))
        self.screen.blit(self.p[11], (88*3, 100))
        self.screen.blit(self.p[13], (40, 150))
        self.screen.blit(self.p[14], (88, 150))
        self.screen.blit(self.p[15], (88+48, 150))

        self.screen.blit(pygame.font.Font(None, 24).render(
            "Press any key", 1, (255, 255, 255)), (416-120, 400-20))
        self.screen.blit(pygame.font.Font(None, 22).render(
            "Coded by "+__author__+" under "+__license__+" license", 1, (255, 255, 255)), (48, 220))
        self.screen.blit(pygame.font.Font(None, 22).render(
            "https://github.com/dakk   "+__email__, 1, (255, 255, 255)), (48, 240))

        pygame.display.update()

        while not intro:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exitGame()

                elif event.type == KEYDOWN:
                    intro = 1
            time.sleep(__sleep__)

        # Finche' il pc e' acceso rigioca
        while 1:
            # Azzera tutto
            self.newGame()
            self.genBlock()
            self.renderGame()

            # Loop di rendering
            while not self.over:
                self.updateGame()
                if self.blockgrid[0][0] == -1:
                    self.genBlock()
                self.keyInputs()
                self.renderGame()
                time.sleep(__sleep__)
                self.time += __sleep__

            # Finito il gioco, visualizza il punteggio e attende
            restart = 0
            print("[*] Game Over")

            self.screen.blit(self.gameover, (0, 0))
            self.screen.blit(pygame.font.Font(None, 36).render(
                "Game Over!", 1, (255, 255, 255)), (20, 20))
            self.screen.blit(pygame.font.Font(None, 24).render(
                "Press any key", 1, (255, 255, 255)), (416-120, 400-20))

            pygame.display.update()

            while not restart:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.exitGame()

                    elif event.type == KEYDOWN:
                        restart = 1
                time.sleep(__sleep__)


def main():
	game = FreeAlchemist()
	game.start()

if __name__ == "__main__":
    main()
