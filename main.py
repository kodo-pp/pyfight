#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from traceback import print_exc 
from threading import Thread, Lock
from time import sleep

import pygame

from load_image import load_image
from run_with_fps import run_with_fps, ExitLoop
from fatal_exceptions import fatal_exceptions
from enemy import Enemy
from player import Player
from health_osd import HealthOSD
from game import GameOver

class Game:
    def __init__(self, window_title):
        # Object initialization
        self.lock = Lock()
        self.do_quit = False
        self.sprites = pygame.sprite.Group()

        # Pygame initialization
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(window_title)

        # Sprites initialization
        self.sprites.add(Enemy(image='enemy.png', game=self, gravity=1700, pos=[500, 200]))

        self.player = Player(game=self, gravity=1700, pos=[300, 200])
        self.sprites.add(self.player)

        self.health_osd = HealthOSD(game=self, pos=[620, 18])
        self.sprites.add(self.health_osd)

    def draw(self):
        with self.lock:
            if self.do_quit:
                raise ExitLoop()

            self.screen.fill((0, 0, 0))
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def process(self):
        with self.lock:
            for event in pygame.event.get():
                self.process_event(event)
            self.process_keys()
            if self.do_quit:
                raise ExitLoop()
            try:
                self.sprites.update()
            except GameOver:
                self.do_quit = True
                self.game_over()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.do_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.do_quit = True

    def process_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.go_left()
        if keys[pygame.K_RIGHT]:
            self.player.go_right()
        if keys[pygame.K_UP]:
            self.player.jump()
        # TODO: add controls
        pass

    @fatal_exceptions
    def draw_loop(self, fps):
        run_with_fps(fps, self.draw)

    @fatal_exceptions
    def process_loop(self, tps):
        run_with_fps(tps, self.process)

    def loop(self, fps, tps):
        draw_thread = Thread(target=self.draw_loop, args=[fps])
        process_thread = Thread(target=self.process_loop, args=[tps])

        draw_thread.start()
        process_thread.start()

        draw_thread.join()
        process_thread.join()

    def game_over(self):
        image = load_image('game_over.png')
        rect = pygame.Rect((0, 0), self.size)
        self.screen.blit(image, rect)
        pygame.display.flip()
        sleep(5)
        raise ExitLoop()

def main():
    game = Game('pyfight')
    game.loop(fps=60, tps=60)

if __name__ == '__main__':
    main()
