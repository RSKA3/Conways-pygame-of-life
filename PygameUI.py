import pygame

import Game
import constants


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Conways PyGame of Life")
    screen = pygame.display.set_mode(constants.screenDimensions, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    tick = 0

    game = Game.Game(constants.initialGridDimension, constants.updateEveryTicks)
    main = Main(game)

    mouseButtons: MouseButtons = MouseButtons()

    while not game.isOver():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.gameOver = True

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        game.paused = not game.paused
                    case pygame.K_RIGHT: # add left arrow button to forward game
                        if game.paused:
                            game.update()
                    case pygame.K_PLUS:
                        game.changeDimensions(-10)
                    case pygame.K_MINUS:
                        game.changeDimensions(10)


            elif event.type == pygame.KEYUP:
                pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseButtons.pressed(event.button, True)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouseButtons.pressed(event.button, False)

        if mouseButtons.isOn():
            main.click(pygame.mouse.get_pos(), game, mouseButtons, tick)

        main.draw(screen, game)
        pygame.display.flip() # updates screen


        if tick % game.speed == 0: # if the tick is divisible by updateEveryTicks then we update the game
            if not game.paused:
                game.update()

        tick += 1
        clock.tick(constants.gameTick)  # limits FPS to 60


    pygame.quit()


class MouseButtons:
    LEFT = False
    MIDDLE = False
    RIGHT = False

    def isOn(self) -> bool: 
        return self.LEFT or self.MIDDLE or self.RIGHT
    
    def pressed(self, button: int, onOff: bool):
        match button:
            case 1:
                self.LEFT = onOff
            case 2:
                self.MIDDLE = onOff
            case 3: 
                self.RIGHT = onOff
    

class Main:
    def __init__(self, game: Game):
        # screens
        self.map: Map           = Map(game)
        self.buttons: Buttons   = Buttons()

        self.mapRect: pygame.Rect           = pygame.Rect()
        self.bottomButtonsRect: pygame.Rect = pygame.Rect()
        self.rightButtonsRect: pygame.Rect  = pygame.Rect()

    def draw(self, surface: pygame.Surface, game: Game):
        surface.fill(constants.mainBoxHex)

        surfaceWidth = surface.get_width()
        surfaceHeight = surface.get_height()

        # map
        self.mapRect.update(surfaceWidth * 0.05, surfaceHeight * 0.05, 
                            surfaceWidth * 0.8, surfaceHeight * 0.8) # This cannot be reassigned for some reason, has to be updated instead
        mapSurface = pygame.Surface((self.mapRect.width, self.mapRect.height))
        self.map.draw(mapSurface, game.getAliveCells())
        surface.blit(mapSurface, dest = (self.mapRect.left, self.mapRect.top))

        # score
        fontSize = int(self.mapRect.top * 0.8)
        roundFont = pygame.font.Font(filename = constants.fontPath, size = fontSize) # init the default font
        scoreSurface = roundFont.render(f"Round: {game.round}", True, "black")
        surface.blit(scoreSurface, (self.mapRect.left, self.mapRect.top - fontSize))

        # gridSize
        fontSize = int(self.mapRect.top * 0.4)
        roundFont = pygame.font.Font(filename = constants.fontPath, size = fontSize) # init the default font
        gridSizeSurface = roundFont.render(f"{game.gridDimension()}x{game.gridDimension()}", True, "black")
        surface.blit(gridSizeSurface, (self.mapRect.right - gridSizeSurface.width, self.mapRect.top - fontSize))

        # buttonsBottom
        self.bottomButtonsRect.update(self.mapRect.left, self.mapRect.top + self.mapRect.height,
                                self.mapRect.width, surfaceHeight * 0.1)
        buttonSurface = pygame.Surface((self.mapRect.width, self.bottomButtonsRect.height))
        self.buttons.drawBottom(buttonSurface, game)
        surface.blit(buttonSurface, dest = (self.mapRect.left, self.mapRect.top + self.mapRect.height))
        
        #buttonsRight

        # buttonsBottom
        self.rightButtonsRect.update(self.mapRect.right, self.mapRect.top + self.mapRect.height / 3,
                                     surfaceWidth * 0.1, surfaceWidth * 0.2)
        rightButtonsSurface = pygame.Surface((self.rightButtonsRect.width, self.rightButtonsRect.height))
        self.buttons.drawRight(rightButtonsSurface, game)
        surface.blit(rightButtonsSurface, dest = (self.rightButtonsRect.left, self.rightButtonsRect.top))


    def click(self, pos: tuple[int, int], game: Game, buttons: MouseButtons, tick: int):
        # Here the idea is to figure out where tf the click happened.
        # map.click(pos[0] - width * 0.1)
        if self.mapRect.collidepoint(pos):
            newPos = (pos[0] - self.mapRect.left, pos[1] - self.mapRect.top)
            self.map.click(newPos, game, buttons)
        elif self.bottomButtonsRect.collidepoint(pos):
            newPos = (pos[0] - self.bottomButtonsRect.left, pos[1] - self.bottomButtonsRect.top)
            self.buttons.clickBottom(newPos, game, buttons, tick)
        elif self.rightButtonsRect.collidepoint(pos):
            newPos = (pos[0] - self.rightButtonsRect.left, pos[1] - self.rightButtonsRect.top)
            self.buttons.clickRight(newPos, game, buttons, tick)
   

class Map:
    def __init__(self, game: Game):
        self.game: Game = game

        self.lastSurface = pygame.Surface((0, 0))

    def draw(self, surface: pygame.Surface, cells: list[tuple[int, int]]):
        surface.fill(constants.mapBackgroundHex)
        
        if self.game.gridDimension() < constants.stopDrawingGridLines:
            self._drawGrid(surface)
        self._drawCells(surface, cells)

        self.lastSurface = surface

    def _drawCells(self, surface, cells) -> None:
        squareWidth = surface.get_width() / self.game.gridDimension()
        squareHeight = surface.get_height() / self.game.gridDimension()

        for cell in cells:
            x, y = cell
            rect = pygame.Rect(x * squareWidth, y * squareHeight, squareWidth, squareHeight)
            pygame.draw.rect(surface, constants.cellHex, rect)


    def _drawGrid(self, surface):
        squareWidth = surface.get_width() / self.game.gridDimension()
        squareHeight = surface.get_height() / self.game.gridDimension()

        for x in range(self.game.gridDimension()):
            for y in range(self.game.gridDimension()):
                rect = pygame.Rect(squareWidth * x, squareHeight * y,
                                   squareWidth, squareHeight)
                pygame.draw.rect(surface, "white", rect, 1)

    def click(self, pos: tuple[int, int], game: Game, buttons: MouseButtons):
        squareWidth = self.lastSurface.get_width() / self.game.gridDimension()
        squareHeight = self.lastSurface.get_height() / self.game.gridDimension()

        x, y = pos
        
        pos = (int(x / squareWidth), int(y / squareHeight))

        if buttons.LEFT:
            game.addCell(pos)
        if buttons.RIGHT: # I am not using elif incase the user might want to remove and add at same time? idfk?
            game.removeCell(pos)


class Buttons:
    def __init__(self):
        # icons
        self.forwardButton  = pygame.image.load(constants.forwardIconPath)
        self.pauseButton    = pygame.image.load(constants.pauseIconPath)
        self.playButton     = pygame.image.load(constants.playIconPath)
        self.zoomInButton   = pygame.image.load(constants.zoomInIconPath)
        self.zoomOutButton  = pygame.image.load(constants.zoomOutIconPath)

        # rects
        self.forwardButtonRect      = self.forwardButton.get_rect()
        self.pausePlayButtonRect    = self.pauseButton.get_rect() # this corresponds to both pauseButton and playbutton
        self.zoomInButtonRect       = self.zoomInButton.get_rect()
        self.zoomOutButtonRect      = self.zoomOutButton.get_rect()
        self.sliderRect             = pygame.Rect()

        # buttonTimers
        self.lastPressedPause   = 0
        self.lastPressedForward = 0
        self.lastPressedZoomIn  = 0
        self.lastPressedZoomOut = 0

        self.sliderDotPos = -1


    def drawBottom(self, surface: pygame.Surface, game: Game):
        surface.fill(constants.buttonBoxHex)

        surfaceWidth = surface.get_width()
        surfaceHeight = surface.get_height()

        
        # Play/Pause
        pause = self.pauseButton if game.paused else self.playButton 
        # lets take the min of surfaceHeight * 0.5 and surfaceWidth * 0.5
        pausePlaySize = min(surfaceHeight, surfaceWidth) * 0.8 # In case user stretches the screen really skinny and long
        self.pausePlayButtonRect.update(surfaceWidth * 0.05, surfaceHeight * 0.1,
                                        pausePlaySize, pausePlaySize)
        pause = pygame.transform.scale(pause, 
                                       (self.pausePlayButtonRect.width, self.pausePlayButtonRect.height))
        surface.blit(pause, (self.pausePlayButtonRect.left, self.pausePlayButtonRect.top))

        # Forward
        forwardSize = min(surfaceHeight, surfaceWidth) * 0.8
        self.forwardButtonRect.update(self.pausePlayButtonRect.right + surfaceWidth * 0.05, surfaceHeight * 0.1,
                                      forwardSize, forwardSize)
        forward = pygame.transform.scale(self.forwardButton, 
                                       (self.forwardButtonRect.width, self.forwardButtonRect.height))
        surface.blit(forward, (self.forwardButtonRect.left, self.forwardButtonRect.top))

        # Slider
        # There is a discreptancy between where we draw the line and where it can be clicked.
        # To solve this we need to place the slider in the middle of the rect
        self.sliderRect = pygame.Rect(surfaceWidth * 0.5, surfaceHeight * 0.1, # this is where the top is
                                      surfaceWidth * 0.4, surfaceHeight * 0.8)
        pygame.draw.rect(surface, "white", (self.sliderRect.left, self.sliderRect.centery, self.sliderRect.width, 2))

        if self.sliderDotPos == -1:
            self.sliderDotPos = self.sliderRect.centerx

        pygame.draw.circle(surface, "black", (self.sliderDotPos, self.sliderRect.centery), 5)

        surface = pygame.draw.rect(surface, "white", surface.get_rect(), 1) # Add border to box


    def drawRight(self, surface: pygame.Surface, game: Game):
        surface.fill(constants.buttonBoxHex)

        surfaceWidth = surface.get_width()
        surfaceHeight = surface.get_height()

        # zoom in button
        minWidthHeight = min(surfaceHeight, surfaceWidth)
        self.zoomInButtonRect.update(minWidthHeight * 0.1, minWidthHeight * 0.1,
                                        minWidthHeight * 0.8, minWidthHeight * 0.8)
        zoomInButtonSurface = pygame.transform.scale(self.zoomInButton, (self.zoomInButtonRect.width, self.zoomInButtonRect.height))
        surface.blit(zoomInButtonSurface, (self.zoomInButtonRect.left, self.zoomInButtonRect.top))

        # zoom out button
        self.zoomOutButtonRect.update(minWidthHeight * 0.1, self.zoomInButtonRect.bottom + minWidthHeight * 0.1,
                                      minWidthHeight * 0.8, minWidthHeight * 0.8)
        zoomOutButtonSurface = pygame.transform.scale(self.zoomOutButton, (self.zoomOutButtonRect.width, self.zoomOutButtonRect.height))
        surface.blit(zoomOutButtonSurface, (self.zoomOutButtonRect.left, self.zoomOutButtonRect.top))

        surface = pygame.draw.rect(surface, "white", surface.get_rect(), 1)


    def clickBottom(self, pos: tuple[int, int], game: Game, buttons: MouseButtons, tick: int):
        if self.pausePlayButtonRect.collidepoint(pos) and tick - self.lastPressedPause >= constants.buttonsCanBePressedEveryTicks:
            self.lastPressedPause = tick
            game.paused = not game.paused
        elif self.forwardButtonRect.collidepoint(pos) and game.paused and tick - self.lastPressedForward >= constants.buttonsCanBePressedEveryTicks: # no point in being able to forward wile game running
            self.lastPressedForward = tick
            game.update()
        elif self.sliderRect.collidepoint(pos):
            self.sliderDotPos = pos[0]
            game.speed = constants.maxSpeed - int(((self.sliderDotPos - self.sliderRect.left) / self.sliderRect.width) * constants.maxSpeed) # we want left to be 10 and right to be 1
            print(game.speed)


    def clickRight(self, pos: tuple[int, int], game: Game, buttons: MouseButtons, tick: int):
        if self.zoomInButtonRect.collidepoint(pos) and tick - self.lastPressedZoomIn >= constants.buttonsCanBePressedEveryTicks:
            self.lastPressedZoomIn = tick
            game.changeDimensions(-10)
        elif self.zoomOutButtonRect.collidepoint(pos) and tick - self.lastPressedZoomOut >= constants.buttonsCanBePressedEveryTicks: # no point in being able to forward wile game running
            self.lastPressedZoomOut = tick
            game.changeDimensions(10)

if __name__ == "__main__":
    main()