"""
Five Twelve (model.py)
by Alex JPS
2023-01-23
CS 211

The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 

Credits:
https://realpython.com/python-range/#decrementing-with-range
"""

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4

class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other: "Vec") -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)


class Tile(GameElement):
    """Tile object that takes one space on the board and has a int value"""

    def __init__(self, pos: Vec, value: int):
        super().__init__()
        self.row = pos.x
        self.col = pos.y
        self.value = value

    def __repr__(self):
        """Does not use 'contstructor' form, more useful for debugging here"""
        return f"Tile[{self.row},{self.col}]:{self.value}"

    def __str__(self):
        """Returns tile value as string"""
        return str(self.value)

    def move_to(self, new_pos: Vec):
        """Updates tile's knowldedge of its positon and alerts view"""
        self.row = new_pos.x
        self.col = new_pos.y
        self.notify_all(GameEvent(EventKind.tile_updated, self))

    def __eq__(self, other: "Tile"):
        """Tiles are equal if their values are equal"""
        return self.value == other.value

    def merge(self, other: "Tile"):
        """When sliding into other tile of equal value, replace it and double my value"""
        # This tile incorporates the value of the other tile
        self.value = self.value + other.value
        self.notify_all(GameEvent(EventKind.tile_updated, self))
        # The other tile has been absorbed.  Resistance was futile.
        other.notify_all(GameEvent(EventKind.tile_removed, other))

class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    def __init__(self, rows: int = 4, cols: int = 4):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.tiles = []
        # creates empty board (list of lists) w/ dimensions
        for row in range(rows):
            row_tiles = []
            for col in range(cols):
                row_tiles.append(None)
            self.tiles.append(row_tiles)

    def __getitem__(self, pos: Vec) -> Tile:
        """Allows referencing tiles like board[Vec(0, 0)]"""
        return self.tiles[pos.x][pos.y]

    def __setitem__(self, pos: Vec, tile: Tile):
        """Allows setting tiles like board[Vec(0, 0)] = Tile object"""
        self.tiles[pos.x][pos.y] = tile

    def _empty_positions(self) -> List[Vec]:
        """Return a list of empty positions of unoccupied spaces (None values)"""
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.tiles[row][col] is None:
                    empty.append(Vec(row, col))
        return empty

    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        if self._empty_positions() == []:
            return False
        else:
            return True

    def place_tile(self, value=None):
        """Place a tile on a randomly chosen empty square."""
        empties = self._empty_positions()
        assert len(empties) > 0
        choice = random.choice(empties)
        row, col = choice.x, choice.y
        if value is None:
            # 0.1 probability of 4
            value = 4 if random.random() < 0.1 else 2
        new_tile = Tile(Vec(row, col), value)
        self.tiles[row][col] = new_tile
        self.notify_all(GameEvent(EventKind.tile_created, new_tile))

    def to_list(self) -> List[List[int]]:
        """Test scaffolding: print board tiles in list of lists, 0 = empty space"""
        result = []
        for row in self.tiles:
            row_values = []
            for col in row:
                if col is None:
                    row_values.append(0)
                else:
                    row_values.append(col.value)
            result.append(row_values)
        return result

    def from_list(self, values: List[List[int]]):
        """Test scaffolding: set board tiles to given values, 0 = empty space"""
        for row in range(len(values)):
            for col in range(len(values[0])):
                if values[row][col] == 0:
                    new_tile = None
                else:
                    new_tile = Tile(Vec(row, col), values[row][col])
                self.tiles[row][col] = new_tile

    def in_bounds(self, pos: Vec) -> bool:
        """"Is given position vector a legal position on the board?"""
        if pos.x in range(len(self.tiles)) and pos.y in range(len(self.tiles[0])):
            return True
        else:
            return False

    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        """Move tile at given position to new position"""
        # Call the tile's move_to method
        assert isinstance(self[old_pos], Tile)
        moving_tile = self[old_pos]
        moving_tile.move_to(new_pos)
        self.tiles[new_pos.x][new_pos.y] = moving_tile
        self.tiles[old_pos.x][old_pos.y] = None
        # should i also update the board list of lists?

    def slide(self, pos: Vec,  dir: Vec):
        """Slide tile at pos.x, pos.y (if any)
        in direction (dir.x, dir.y) until it bumps into
        another tile or the edge of the board.
        """ 
        if self[pos] is None:
            return
        while True:
            new_pos = pos + dir
            if not self.in_bounds(new_pos):
                break
            if self[new_pos] is None:
                self._move_tile(pos, new_pos)
            elif self[pos] == self[new_pos]:
                self[pos].merge(self[new_pos])
                self._move_tile(pos, new_pos)
                break  # Stop moving when we merge with another tile
            else:
                # Stuck against another tile
                break
            pos = new_pos

    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        result = 0
        end_board = self.to_list()
        for i in end_board:
            for j in i:
                result += j
        return result

    def up(self):
        """Move all tiles up in correct order"""
        slide_vec = Vec(-1, 0)
        for row in range(self.rows):
            for col in range(self.cols):
                self.slide(Vec(row, col), slide_vec)

    def left(self):
        """Move all tiles left in correct order"""
        slide_vec = Vec(0, -1)
        for row in range(self.rows):
            for col in range(self.cols):
                self.slide(Vec(row, col), slide_vec)

    def down(self):
        """Move all tiles down in correct order"""
        slide_vec = Vec(1, 0)
        for row in range(self.rows -1, -1, -1):
            for col in range(self.cols):
                self.slide(Vec(row, col), slide_vec)

    def right(self):
        """Move all tiles right in correct order"""
        slide_vec = Vec(0, 1)
        for row in range(self.rows):
            for col in range(self.cols -1, -1, -1):
                self.slide(Vec(row, col), slide_vec)