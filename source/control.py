import pygame as pg
import time

from . import constants as c
from .components.main import Main
from . import game
from .utils import get_image

class Control:
    def __init__(self) -> None:
        logo = get_image(c.FILE_PATH, c.LOGO_ICON)
        pg.display.set_icon(logo)
        self.game = game.Game(c.INITIAL_GRID_DIMENSION)
        self.main = Main()

        pg.font.init()
        pg.display.set_caption("Conways PyGame of Life")
        self.clock = pg.time.Clock()
        h = int(pg.display.Info().current_h * c.INIT_SIZE_OF_WINDOW) # Gets window height and then sets size according to it.
        self.screen = pg.display.set_mode((h, h), pg.RESIZABLE)

        self.mouse_click: list[bool] = [False, False] # Left and Right

        self.ticks_per_update = c.INITIAL_TICKS_PER_UPDATE
        self.ticks_since_update = 0

        self.settings = c.INIT_SETTINGS


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.gameOver = True

            elif event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        self.settings[c.PAUSED] = not self.settings[c.PAUSED]
                    case pg.K_RIGHT: # add left arrow button to forward game
                        if self.settings[c.PAUSED]:
                            self.game.update()
                    case pg.K_PLUS:
                        self.game.changeDimensions(-c.CHANGE_DIMENSIONS_BY)
                    case pg.K_MINUS:
                        self.game.changeDimensions(c.CHANGE_DIMENSIONS_BY)

            elif event.type == pg.KEYUP:
                pass
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                (self.mouse_click[0], _, self.mouse_click[1]) = pg.mouse.get_pressed()

            elif event.type == pg.MOUSEBUTTONUP:
                (self.mouse_click[0], _, self.mouse_click[1]) = pg.mouse.get_pressed()


    def update(self):
        if True in self.mouse_click: # if either button is pressed
            self.settings = self.main.click(pg.mouse.get_pos(), self.mouse_click, self.game, self.settings)
        
        self.main.draw(self.screen, self.game, self.settings)

        # check if need to be updated
        if not self.settings[c.PAUSED] and self.ticks_since_update >= self.settings[c.TICKS_PER_UPDATE]:
            self.game.update()
            self.ticks_since_update = 0
        else:
            self.ticks_since_update += 1


    def run(self):
        while not self.game.isOver():
            self.event_loop()
            self.update()

            pg.display.update()

            self.settings[c.TICK] += 1
            self.clock.tick(c.TICK_SPEED)