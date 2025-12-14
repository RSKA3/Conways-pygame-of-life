import pygame as pg

from ..game import Game
from .. import constants as c

from ..utils import get_image

class Bottom_buttons:
    def __init__(self):
        # icons
        self.forward_button  = get_image(c.FILE_PATH, c.FORWARD_ICON)
        self.pause_button    = get_image(c.FILE_PATH, c.PAUSE_ICON)
        self.play_button     = get_image(c.FILE_PATH, c.PLAY_ICON)

        # rects
        self.forward_button_rect      = self.forward_button.get_rect()
        self.pause_play_button_rect    = self.pause_button.get_rect() # this corresponds to both pauseButton and playbutton
        self.slider_rect             = pg.Rect()

        # buttonTimers
        self.lastPressedPause   = 0
        self.lastPressedForward = 0

        self.sliderDotPos = 0.5 # the middle of the slider


    def draw(self, surface: pg.Surface, settings: dict):
        surface.fill(c.BUTTON_COLOR)

        surfaceWidth = surface.get_width()
        surfaceHeight = surface.get_height()
        
        # Play/Pause
        pause = self.pause_button if settings[c.PAUSED] else self.play_button 
        # lets take the min of surfaceHeight * 0.5 and surfaceWidth * 0.5
        pausePlaySize = min(surfaceHeight, surfaceWidth) * 0.8 # In case user stretches the screen really skinny and long
        self.pause_play_button_rect.update(surfaceWidth * 0.05, surfaceHeight * 0.1,
                                        pausePlaySize, pausePlaySize)
        pause = pg.transform.scale(pause, 
                                       (self.pause_play_button_rect.width, self.pause_play_button_rect.height))
        surface.blit(pause, (self.pause_play_button_rect.left, self.pause_play_button_rect.top))

        # Forward
        forwardSize = min(surfaceHeight, surfaceWidth) * 0.8
        self.forward_button_rect.update(self.pause_play_button_rect.right + surfaceWidth * 0.05, surfaceHeight * 0.1,
                                      forwardSize, forwardSize)
        forward = pg.transform.scale(self.forward_button, 
                                       (self.forward_button_rect.width, self.forward_button_rect.height))
        surface.blit(forward, (self.forward_button_rect.left, self.forward_button_rect.top))

        # Slider
        self.sliderDotPos = (settings[c.TICKS_PER_UPDATE] - c.MIN_TICKS_PER_UPDATE) / (c.MAX_TICKS_PER_UPDATE  - c.MIN_TICKS_PER_UPDATE)
        self.slider_rect = pg.Rect(surfaceWidth * 0.5, surfaceHeight * 0.1, # this is where the top is
                                      surfaceWidth * 0.4, surfaceHeight * 0.8)
        pg.draw.rect(surface, "white", (self.slider_rect.left, self.slider_rect.centery, self.slider_rect.width, 2))

        pg.draw.circle(surface, "black", (self.slider_rect.left + self.slider_rect.width * self.sliderDotPos, self.slider_rect.centery), 5)

        pg.draw.rect(surface, "white", surface.get_rect(), 1) # Add border to box


    def click(self, pos: tuple[int, int], game: Game, settings: dict) -> dict:
        if self.pause_play_button_rect.collidepoint(pos) and settings[c.TICK] - self.lastPressedPause >= c.buttonsCanBePressedEveryTicks:
            self.lastPressedPause = settings[c.TICK]
            settings[c.PAUSED] = not settings[c.PAUSED]

        elif self.forward_button_rect.collidepoint(pos) and settings[c.PAUSED] and settings[c.TICK] - self.lastPressedForward >= c.buttonsCanBePressedEveryTicks: # no point in being able to forward wile game running
            self.lastPressedForward = settings[c.TICK]
            game.update()

        elif self.slider_rect.collidepoint(pos):
            slider_pos = (pos[0] - self.slider_rect.left) / self.slider_rect.width
            settings[c.TICKS_PER_UPDATE] = round(c.MIN_TICKS_PER_UPDATE + (c.MAX_TICKS_PER_UPDATE - c.MIN_TICKS_PER_UPDATE) * slider_pos) # we want left to be 10 and right to be 1
        
        return settings