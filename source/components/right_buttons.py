import pygame as pg

from ..game import Game
from .. import constants as c
from ..utils import get_image

class Right_buttons:
    def __init__(self) -> None:
        self.zoom_in_button   = get_image(c.FILE_PATH, c.ZOOM_IN_ICON)
        self.zoom_out_button  = get_image(c.FILE_PATH, c.ZOOM_OUT_ICON)

        self.zoom_in_button_rect       = self.zoom_in_button.get_rect()
        self.zoom_out_button_rect      = self.zoom_out_button.get_rect()

        self.last_pressed_zoom_in  = 0
        self.last_pressed_zoom_out = 0


    def draw(self, surface: pg.Surface):
        surface.fill(c.BUTTON_COLOR)

        width, height = surface.get_size()

        # zoom in button
        minWidthHeight = min(width, height)
        self.zoom_in_button_rect.update(minWidthHeight * 0.1, minWidthHeight * 0.1,
                                        minWidthHeight * 0.8, minWidthHeight * 0.8)
        zoomInButtonSurface = pg.transform.scale(self.zoom_in_button, (self.zoom_in_button_rect.width, self.zoom_in_button_rect.height))
        surface.blit(zoomInButtonSurface, (self.zoom_in_button_rect.left, self.zoom_in_button_rect.top))

        # zoom out button
        self.zoom_out_button_rect.update(minWidthHeight * 0.1, self.zoom_in_button_rect.bottom + minWidthHeight * 0.1,
                                      minWidthHeight * 0.8, minWidthHeight * 0.8)
        zoomOutButtonSurface = pg.transform.scale(self.zoom_out_button, (self.zoom_out_button_rect.width, self.zoom_out_button_rect.height))
        surface.blit(zoomOutButtonSurface, (self.zoom_out_button_rect.left, self.zoom_out_button_rect.top))

        pg.draw.rect(surface, "white", surface.get_rect(), 1)

    def click(self, pos: tuple[int, int], game: Game, settings: dict[str, int]):
        if self.zoom_in_button_rect.collidepoint(pos) and settings[c.TICK] - self.last_pressed_zoom_in >= c.buttonsCanBePressedEveryTicks:
            self.last_pressed_zoom_in = settings[c.TICK]
            game.changeDimensions(-10)
        elif self.zoom_out_button_rect.collidepoint(pos) and settings[c.TICK] - self.last_pressed_zoom_out >= c.buttonsCanBePressedEveryTicks: # no point in being able to forward wile game is running
            self.last_pressed_zoom_out = settings[c.TICK]
            game.changeDimensions(10)
        return settings