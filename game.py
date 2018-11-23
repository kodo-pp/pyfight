import random as rd
from time import sleep, time
from threading import Thread, Lock

import pygame

from load_image import load_image
from run_with_fps import run_with_fps, ExitLoop
from fatal_exceptions import fatal_exceptions
from enemy import Enemy
from player import Player
from health_osd import HealthOSD
from game_over import GameOver

MAX_ENEMY_HP = 8
MIN_ENEMY_HP = 3

class Game:
    def __init__(self):
        # Object initialization
        self.lock = Lock()
        self.do_quit = False
        self.sprites = pygame.sprite.Group()
        self.add_queue = []
        self.last_score = -1
        self.score = 0

        # Pygame initialization
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.update_score()

        # Sprites initialization
        self.player1 = Player(
            base_image='player1.png',
            hit_image='player1_hit.png',
            hit_particle_image='player1_hit_particle.png',
            game=self,
            gravity=1700,
            pos=[300, 200]
        )
        self.player2 = Player(
            base_image='player2.png',
            hit_image='player2_hit.png',
            hit_particle_image='player2_hit_particle.png',
            game=self,
            gravity=1700,
            pos=[500, 200]
        )
        self.sprites.add(self.player1)
        self.sprites.add(self.player2)

        self.health_osd1 = HealthOSD(game=self, target=self.player1, pos=[180, 18])
        self.health_osd2 = HealthOSD(game=self, target=self.player2, pos=[620, 18])
        self.sprites.add(self.health_osd1)
        self.sprites.add(self.health_osd2)

        self.last_mob_spawn = None

    def get_nearest_player(self, pos):
        if self.player1.dead:
            return self.player2
        if self.player2.dead:
            return self.player1
        d1 = abs(self.player1.rect.center[0] - pos[0])
        d2 = abs(self.player2.rect.center[0] - pos[0])
        if d1 < d2:
            return self.player1
        else:
            return self.player2

    def get_random_player(self):
        if self.player1.dead:
            return self.player2
        if self.player2.dead:
            return self.player1
        return [self.player1, self.player2][rd.randrange(0, 2)]

    def update_score(self):
        if self.last_score == self.score:
            return
        self.last_score = self.score
        pygame.display.set_caption('pygame: score: {}'.format(self.score))

    def maybe_spawn_mobs(self):
        SPAWN_MOB_EACH = 1.0
        cur_time = time()
        if self.last_mob_spawn is None:
            self.last_mob_spawn = cur_time
            return False
        if cur_time - self.last_mob_spawn < SPAWN_MOB_EACH:
            return False
        self.last_mob_spawn = cur_time
        self.sprites.add(
            Enemy(
                health=rd.randint(MIN_ENEMY_HP, MAX_ENEMY_HP),
                image='enemy.png',
                game=self,
                gravity=1700,
                pos=[rd.randint(0, 800), 0]
            )
        )
        return True

    def draw(self):
        with self.lock:
            self.update_score()
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
            if self.player1.dead and self.player2.dead:
                self.do_quit = True
                self.game_over()
            if self.do_quit:
                raise ExitLoop()
            self.sprites.add(*self.add_queue)
            self.add_queue = []
            self.remove_dead_sprites()
            self.sprites.update()
            self.maybe_spawn_mobs()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.do_quit = True
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_q:
        #        self.do_quit = True

    def process_keys(self):
        keys = pygame.key.get_pressed()
        if not self.player2.dead:
            if keys[pygame.K_LEFT]:
                self.player2.go_left()
            if keys[pygame.K_RIGHT]:
                self.player2.go_right()
            if keys[pygame.K_UP]:
                self.player2.jump()
            if keys[pygame.K_m]:
                self.player2.maybe_shoot()
        if not self.player1.dead:
            if keys[pygame.K_s]:
                self.player1.go_left()
            if keys[pygame.K_f]:
                self.player1.go_right()
            if keys[pygame.K_e]:
                self.player1.jump()
            if keys[pygame.K_1]:
                self.player1.maybe_shoot()

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

    def add_sprite(self, sprite):
        self.add_queue.append(sprite)

    def game_over(self):
        self.health_osd1.update()
        self.health_osd2.update()
        self.sprites.draw(self.screen)
        image = load_image('game_over.png')
        rect = pygame.Rect((0, 0), self.size)
        self.screen.blit(image, rect)
        pygame.display.flip()
        sleep(5)
        raise ExitLoop()

    def remove_dead_sprites(self):
        to_remove = []
        for i in self.sprites.sprites():
            if i.dead:
                to_remove.append(i)
        self.sprites.remove(*to_remove)
