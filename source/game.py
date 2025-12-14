import pygame as pg

from . import constants as c

class Game:
    def __init__(self, gridDimension: int):
        self.grid = Grid(gridDimension)

        self.gameOver   = False
        self.round      = 0

    def isOver(self):
        return self.gameOver
    
    def update(self):
        self.round += 1
        self.grid.updateGrid()


    # related to Grid
    def getAliveCells(self):
        return self.grid.alive_cells

    def removeCell(self, cell: tuple[int, int]) -> None:
        self.grid.removeCell(cell)

    def addCell(self, cell: tuple[int, int]) -> None:
        self.grid.addCell(cell)

    def changeDimensions(self, amount: int):
        self.grid.updateGridDimension(amount)

    def get_grid_dimension(self):
        return self.grid.gridDimension



class Grid:
    def __init__(self, gridDimension: int, initial_cells: list[tuple[int, int]] = None):
        self.gridDimension = gridDimension

        self.alive_cells: set[tuple[int, int]] = set()
        
        if initial_cells != None:
            self.addCellsToGrid(initial_cells)

    
    def updateGrid(self) -> None:
        newGrid = set()

        for cell in self.get_cells_to_be_updated():     # N + N * 9
                n = self.countAliveNeighbours(cell)     # N * 9 * N
                if self.cellIsAlive(cell):  # ALIVE     # N calltime
                    if n == 2 or n == 3:
                        newGrid.add(cell)
                else:                       # DEAD
                    if n == 3:
                        newGrid.add(cell)

        self.alive_cells = newGrid

    def get_cells_to_be_updated(self):
        cells = set()
        for cell in self.alive_cells:
            cells.update(self.get_all_neighbours(cell))
        return set(cells)

    def countAliveNeighbours(self, cell: tuple[int, int]) -> int: 
        return len(self.get_alive_neighbours(cell))
    
    def get_alive_neighbours(self, cell: tuple[int, int]) -> set[tuple[int, int]]: # returns alive neigbouring cells
        k = [-1, 0, 1]
        neighbours = set()
        for i in k:
            for j in k:
                x, y = cell
                newCell = (x + i , y + j)
                if (newCell != cell) and self.cellIsAlive(newCell): # newCell not same cell and cell is alive
                    neighbours.add(newCell)
        return neighbours
    
    def get_all_neighbours(self, cell: tuple[int, int]) -> set[tuple[int, int]]: # returns all neigbouring cells in bounds, including itself
        k = [-1, 0, 1]
        neighbours = set()
        for i in k:
            for j in k:
                x, y = cell
                newCell = (x + i , y + j)
                if self.isCellInBounds(newCell):
                    neighbours.add(newCell)
        return neighbours

    def isCellInBounds(self, cell: tuple[int, int]) -> bool:
        x, y = cell
        return 0 <= x and x < self.gridDimension and 0 <= y and y < self.gridDimension

    # setters & getters
    def addCell(self, cell: tuple[int, int]):
        if self.isCellInBounds(cell):
            self.alive_cells.add(cell)
        else:
            print(f"WARNING: cell: ({cell}) not in bounds")

    def addCellsToGrid(self, cells: list[tuple[int, int]]):
        for cell in cells:
            self.addCell(cell)

    def removeCell(self, cell: tuple[int, int]):
        self.alive_cells.discard(cell)

    def cellIsAlive(self, cell):
        return cell in self.alive_cells
    
    def updateGridDimension(self, amount: int):
        newDimension = self.gridDimension + amount
        if newDimension >= c.MIN_GRID_DIMENSION and newDimension <= c.MAX_GRID_DIMENSION:
            self.gridDimension = newDimension
