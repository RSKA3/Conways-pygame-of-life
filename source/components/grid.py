import pygame as pg

from .. import constants as c
from ..game import Game

class Grid:
    def __init__(self):
        self.lastSurface = pg.Surface((0, 0))

    def draw(self, surface: pg.Surface, game: Game):
        surface.fill(c.MAP_BACKGROUND_COLOR)
        
        if game.get_grid_dimension() < c.stopDrawingGridLines:
            self._drawGrid(surface, game)
        self._drawCells(surface, game)

        self.lastSurface = surface

    def _drawCells(self, surface: pg.Surface, game: Game) -> None:
        squareWidth = surface.get_width() / game.get_grid_dimension()
        squareHeight = surface.get_height() / game.get_grid_dimension()

        for cell in game.getAliveCells():
            x, y = cell
            rect = pg.Rect(x * squareWidth, y * squareHeight, squareWidth, squareHeight)
            pg.draw.rect(surface, c.CELL_COLOR, rect)


    def _drawGrid(self, surface: pg.Surface, game: Game):
        squareWidth = surface.get_width() / game.get_grid_dimension()
        squareHeight = surface.get_height() / game.get_grid_dimension()

        for x in range(game.get_grid_dimension()):
            for y in range(game.get_grid_dimension()):
                rect = pg.Rect(squareWidth * x, squareHeight * y,
                                   squareWidth, squareHeight)
                pg.draw.rect(surface, "white", rect, 1)

    def click(self, pos: tuple[int, int], buttons: list[bool], game: Game, settings: dict[str, int]):
        squareWidth = self.lastSurface.get_width() / game.get_grid_dimension()
        squareHeight = self.lastSurface.get_height() / game.get_grid_dimension()

        x, y = pos
        
        pos = (int(x / squareWidth), int(y / squareHeight))

        if buttons[0]:
            game.addCell(pos)
        if buttons[1]: # I am not using elif incase the user might want to remove and add at same time? idfk?
            game.removeCell(pos)

        return settings