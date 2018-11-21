#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from load_image import load_image
from run_with_fps import run_with_fps, ExitLoop
from threading import Thread, Lock

from ball import BallEntity


class Game:
    def __init__(self):
        # Object initialization
        self.lock = Lock()
        self.do_quit = False

        # Pygame initialization
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)

        # Entities initialization
        self.ball1 = BallEntity(texture_name='ball1.png')
        self.ball2 = BallEntity(texture_name='ball2.png')
        self.speed1 = [2, 2]
        self.speed2 = [5, -3]

    def draw(self):
        with self.lock:
            if self.do_quit:
                raise ExitLoop()

            self.screen.fill((0, 0, 0))
            self.ball1.draw(self.screen)
            self.ball2.draw(self.screen)
            pygame.display.flip()

    def process(self):
        with self.lock:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.do_quit = True
            if self.do_quit:
                raise ExitLoop()

            self.speed1 = self.ball1.bounced_move(size=self.size, speed=self.speed1)
            self.speed2 = self.ball2.bounced_move(size=self.size, speed=self.speed2)

    def draw_loop(self, fps):
        run_with_fps(fps, self.draw)

    def process_loop(self, tps):
        run_with_fps(tps, self.process)

    def loop(self, fps, tps):
        draw_thread = Thread(target=self.draw_loop, args=[fps])
        process_thread = Thread(target=self.process_loop, args=[tps])

        draw_thread.start()
        process_thread.start()

        draw_thread.join()
        process_thread.join()


def main():
    game = Game()
    game.loop(fps=60, tps=60)

if __name__ == '__main__':
    main()
