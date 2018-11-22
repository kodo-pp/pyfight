#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game import Game

def main():
    game = Game()
    game.loop(fps=60, tps=60)

if __name__ == '__main__':
    main()
