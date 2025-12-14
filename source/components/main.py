import pygame as pg

from .grid import Grid
from .bottom_buttons import Bottom_buttons
from .right_buttons import Right_buttons

from .. import constants as c
from ..game import Game
from ..utils import get_font

class Main:
    def __init__(self):

        # screens
        self.grid: Grid = Grid()
        self.bottom_buttons: Bottom_buttons = Bottom_buttons()
        self.right_buttons: Right_buttons = Right_buttons()

        # rects
        self.gridRect: pg.Rect = pg.Rect()
        self.bottom_buttons_rect: pg.Rect = pg.Rect()
        self.right_buttons_rect: pg.Rect  = pg.Rect()

    def draw(self, surface: pg.Surface, game: Game, settings: dict):
        surface.fill(c.MAIN_BOX_COLOR)

        self.draw_grid(surface, game)
        self.draw_score(surface, game)
        self.draw_grid_size(surface, game)
        self.draw_bottom_buttons(surface, settings) # Best style to only pass where needed
        self.draw_right_buttons(surface)


    def draw_grid(self, surface: pg.Surface, game: Game) -> None:
        width, height = surface.size
        self.gridRect.update(width * c.GRID_MULTIPLE["left"], height * c.GRID_MULTIPLE["top"], 
                             width * c.GRID_MULTIPLE["width"], height * c.GRID_MULTIPLE["height"]) # Rects cannot be reassigned, has to be update():d instead
        mapSurface = pg.Surface((self.gridRect.width, self.gridRect.height))
        self.grid.draw(mapSurface, game)
        surface.blit(mapSurface, dest = (self.gridRect.left, self.gridRect.top))

    def draw_score(self, surface: pg.Surface, game: Game) -> None:
        font_size = int(self.gridRect.top * 0.8)
        font = get_font(c.FILE_PATH, c.FONT_NAME, font_size) # init the default font
        scoreSurface = font.render(f"Round: {game.round}", True, "black")
        surface.blit(scoreSurface, (self.gridRect.left, self.gridRect.top - font_size))

    def draw_grid_size(self, surface: pg.Surface, game: Game) -> None:
        font_size = int(self.gridRect.top * 0.4)
        font = get_font(c.FILE_PATH, c.FONT_NAME, font_size) # init the default font
        gridSizeSurface = font.render(f"{game.get_grid_dimension()}x{game.get_grid_dimension()}", True, "black")
        surface.blit(gridSizeSurface, (self.gridRect.right - gridSizeSurface.width, self.gridRect.top - font_size))

    def draw_bottom_buttons(self, surface: pg.Surface, settings: dict) -> None:
        width, height = surface.size
        self.bottom_buttons_rect.update(self.gridRect.left, self.gridRect.top + self.gridRect.height,
                                      self.gridRect.width, height * 0.1)
        button_surface = pg.Surface((self.gridRect.width, self.bottom_buttons_rect.height))
        self.bottom_buttons.draw(button_surface, settings)
        surface.blit(button_surface, dest = (self.gridRect.left, self.gridRect.top + self.gridRect.height))

    def draw_right_buttons(self, surface: pg.Surface) -> None:
        width, height = surface.size
        self.right_buttons_rect.update(self.gridRect.right, self.gridRect.top + self.gridRect.height / 3,
                                       width * 0.1, height * 0.2)
        button_surface = pg.Surface((self.right_buttons_rect.width, self.right_buttons_rect.height))
        self.right_buttons.draw(button_surface)
        surface.blit(button_surface, dest = (self.right_buttons_rect.left, self.right_buttons_rect.top))


    def click(self, pos: tuple[int, int], buttons: list[bool], game: Game, settings: dict) -> dict:
        # Here the idea is to figure out where tf the click happened.
        # map.click(pos[0] - width * 0.1)
        if self.gridRect.collidepoint(pos):
            newPos = (pos[0] - self.gridRect.left, pos[1] - self.gridRect.top)
            settings = self.grid.click(newPos, buttons, game, settings)

        elif self.bottom_buttons_rect.collidepoint(pos):
            newPos = (pos[0] - self.bottom_buttons_rect.left, pos[1] - self.bottom_buttons_rect.top)
            settings = self.bottom_buttons.click(newPos, game, settings)

        elif self.right_buttons_rect.collidepoint(pos):
            newPos = (pos[0] - self.right_buttons_rect.left, pos[1] - self.right_buttons_rect.top)
            settings = self.right_buttons.click(newPos, game, settings)

        return settings