import pygame

import Grid
import constants

class Game:
    def __init__(self, gridDimension: int, updateEveryTicks: int):
        self.grid = Grid.Grid(gridDimension)

        self.gameOver   = False
        self.paused     = True
        self.round      = 0
        self.speed      = updateEveryTicks

    def isOver(self):
        return self.gameOver
    
    def update(self):
        self.round += 1
        self.grid.updateGrid()


    # related to Grid
    def getAliveCells(self):
        return self.grid.aliveCells

    def removeCell(self, cell: tuple[int, int]) -> None:
        self.grid.removeCell(cell)

    def addCell(self, cell: tuple[int, int]) -> None:
        self.grid.addCell(cell)

    def changeDimensions(self, amount: int):
        self.grid.updateGridDimension(amount)

    def gridDimension(self):
        return self.grid.gridDimension