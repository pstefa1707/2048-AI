from enum import Enum, auto
import random
import copy
import time

#Enum because it cleaner than passing strings or integers relating to moves around
class Moves(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()

class Grid:
    #Grid can adapt to any size, also allows for templates to be followed (Copy previous game state, used for AI)
    def __init__(self, width=4, height=4, template=None):
        self._width = width
        self._height = height
        self._score = 0
        self._grid = []
        #Initialised grid to zeros
        if template == None:
            for row in range(self._height):
                self._grid.append([])
                for i in range(self._width):
                    self._grid[row].append(0)
            self.new_cell()
            self.new_cell()
        #Copies template if template exists            
        else:
            self._width = template.cols()
            self._height = template.rows()
            self._score = template.score()
            self._grid = template

    def move(self, direction):
        #A deep copy is made so temp isn't just a reference to self and isnt mutated
        temp = copy.deepcopy(self)
        #Code to calculate board after move, similar way of processing for each move just requires different transformations on rows/cols
        #Algorithm works by scanning in opposite direction of move, adding like numbers together and then proceeds to squash and move all cells, rearranging rows
        if direction is Moves.RIGHT:
            for row in enumerate(self):
                for cell in reversed(range(self._width)):
                    for o_cell in reversed(range(cell)):
                        if row[1][o_cell] == row[1][cell] and row[1][cell] != 0:
                            row[1][cell] += row[1][o_cell]
                            self._score += row[1][cell]
                            row[1][o_cell] = 0
                            break
                        elif row[1][o_cell] != 0:
                            break
                self[row[0]] = list(reversed(self.squash_row(list(reversed(row[1])))))
        elif direction is Moves.LEFT:
            for row in enumerate(self):
                for cell in range(self._width):
                    for o_cell in range(cell + 1, self._width):
                        if row[1][o_cell] == row[1][cell] and row[1][cell] != 0:
                            row[1][cell] += row[1][o_cell]
                            self._score += row[1][cell]
                            row[1][o_cell] = 0
                            break
                        elif row[1][o_cell] != 0:
                            break
                self[row[0]] = self.squash_row(row[1])
        elif direction is Moves.UP:
            for col_index in range(self._width):
                col = self.get_column(col_index)
                for cell in range(self._height):
                    for o_cell in range(cell + 1, self._height):
                        if col[o_cell] == col[cell] and col[cell] != 0:
                            col[cell] += col[o_cell]
                            self._score += col[cell]
                            col[o_cell] = 0
                            break
                        elif col[o_cell] != 0:
                            break
                col = self.squash_row(col)
                self.set_column(col, col_index)
        elif direction is Moves.DOWN:
            for col_index in range(self._width):
                col = list(reversed(self.get_column(col_index)))
                for cell in range(self._height):
                    for o_cell in range(cell + 1, self._height):
                        if col[o_cell] == col[cell] and col[cell] != 0:
                            col[cell] += col[o_cell]
                            self._score += col[cell]
                            col[o_cell] = 0
                            break
                        elif col[o_cell] != 0:
                            break
                col = list(reversed(self.squash_row(col)))
                self.set_column(col, col_index)

        #If current board is not equal to previous board
        if str(self) != str(temp):
            return self.new_cell()
        #If no more free cells
        elif len(self.free_cells()) == 0: return False
        return True
    
    def get_column(self, col_index):
        return [row[col_index] for row in self]
    
    def set_column(self, col, col_index):
        for row in range(self._width):
            self[row][col_index] = col[row]

    def squash_row(self, row):
        new_row = [i for i in row if i != 0]
        return new_row + [0 for i in range(self._width - len(new_row))]

    def free_cells(self):
        free = []
        for row in range(self._height):
            for column in range(self._width):
                if self[row][column] == 0:
                    free.append((row, column))
        return free
    
    def new_cell(self):
        free = self.free_cells()
        if len(free) == 0:
            return False
        cell = random.choice(free)
        #Same probabilties used in online 2048
        if random.randint(0, 100) < 90:
            self[cell[0]][cell[1]] = 2
        else:
            self[cell[0]][cell[1]] = 4
        return True
    
    def rows(self):
        return self._height

    def cols(self):
        return self._width
    
    def score(self):
        return self._score

    def __repr__(self):
        #Returns readable version of current grid
        string = ""
        for row in self:
            string += str(row)
            string += "\n"
        return string
    
    def __len__(self):
        #Returns total size of grid
        return self._height * self._width
    
    def __getitem__(self, position):
        #Returns positions using index form, allows for iteration!
        return self._grid[position]
    
    def __setitem__(self, position, value):
        #Allows for easy setting of entire rows at a time, abstracting away from "self._grid[x] = y"
        self._grid[position] = value
