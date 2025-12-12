import constants

class Grid:
    def __init__(self, gridDimension: int, initial_cells: list[tuple[int, int]] = None):
        self.gridDimension = gridDimension

        self.aliveCells: list[tuple[int, int]] = []
        
        if initial_cells != None:
            self.addCellsToGrid(initial_cells)

        # what if we only stored the alive cells
    
    def updateGrid(self) -> None:
        newGrid = []

        for cell in self.getCellsToBeUpdated():
                n = self.countAliveNeighbours(cell)
                if self.cellIsAlive(cell):  # ALIVE
                    if n == 2 or n == 3:
                        newGrid.append(cell)
                else:                       # DEAD
                    if n == 3:
                        newGrid.append(cell)

        self.aliveCells = newGrid

    def getCellsToBeUpdated(self):
        cells = []
        for cell in self.aliveCells:
            cells.extend(self.getAllNeighbours(cell))
        return list(set(cells))

    def countAliveNeighbours(self, cell: tuple[int, int]) -> int: 
        return len(self.getAliveNeighbours(cell))
    
    def getAliveNeighbours(self, cell: tuple[int, int]) -> list[tuple[int, int]]: # returns alive neigbouring cells
        k = [-1, 0, 1]
        neighbours = []
        for i in k:
            for j in k:
                x, y = cell
                newCell = (x + i , y + j)
                if (newCell != cell) and self.cellIsAlive(newCell): # newCell not same cell and cell is alive
                    neighbours.append(newCell)
        return neighbours
    
    def getAllNeighbours(self, cell: tuple[int, int]) -> list[tuple[int, int]]: # returns all neigbouring cells in bounds, including itself
        k = [-1, 0, 1]
        neighbours = []
        for i in k:
            for j in k:
                x, y = cell
                newCell = (x + i , y + j)
                if self.isCellInBounds(newCell):
                    neighbours.append(newCell)
        return neighbours

    def isCellInBounds(self, cell: tuple[int, int]) -> bool:
        x, y = cell
        print(x, y, self.gridDimension)
        return 0 <= x and x < self.gridDimension and 0 <= y and y < self.gridDimension

    # setters & getters
    def addCell(self, cell: tuple[int, int]):
        if self.isCellInBounds(cell):
            self.aliveCells.append(cell)
        else:
            print(f"WARNING: cell: ({cell}) not in bounds")

    def addCellsToGrid(self, cells: list[tuple[int, int]]):
        for cell in cells:
            self.addCell(cell)

    def removeCell(self, cell: tuple[int, int], grid: list[list[bool]] = None):

        if grid == None:
            grid = self.aliveCells

        try:
            self.aliveCells.remove(cell)
        except ValueError:
            pass

    def cellIsAlive(self, cell):
        return cell in self.aliveCells
    
    def updateGridDimension(self, amount: int):
        newDimension = self.gridDimension + amount
        if newDimension >= constants.minGridDimension and newDimension <= constants.maxGridDimension:
            self.gridDimension = newDimension
