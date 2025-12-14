import pygame as pg

pg.init()

from source import constants as c
from source.control import Control

if __name__ == "__main__":
    game = Control()
    game.run()
    pg.quit()