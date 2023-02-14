"""
Sudoku Board
by Alex JPS
2023-02-13
CS 211

File that handles the model (board and tiles)
of the MVC structure for Sudoku solver.
"""

# Get configuration from file
from sdk_config import CHOICES, UNKNOWN, ROOT
from sdk_config import NROWS, NCOLS

# Enable logging of errors for debugging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
# Set to logging.DEBUG for more details
log.setLevel(logging.INFO)

# Enum for TileChanged event
import enum

# List for type annotations, e.g. List[List[Tile]]
from typing import List, Sequence, Set

"""Events for model-view-controller interaction"""

class Event(object):
    """Abstract base class of all events, for MVC and other purposes"""
    pass

class Listener(object):
    """Abstract class; subclass me to make useful notifications"""

    def __init__(self):
        """Default constructor for simple listeners without state"""
        pass

    def notify(self, event: Event):
        """Override me in concrete subclasses"""
        raise NotImplementedError("You must override Listener.notify")

class EventKind(enum.Enum):
    TileChanged = 1
    TileGuessed = 2

class TileEvent(Event):
    """Abstract class for events happening to tiles
    Event type to be specified by concrete class"""

    def __init__(self, tile: 'Tile', kind: EventKind):
        self.tile = tile
        self.kind = kind
        # Note 'Tile' type is a forward reference;
        # Tile class is defined below

    def __str__(self):
        """Printed representation includes name of concrete subclass"""
        return f"{repr(self.tile)}"

class TileListener(Listener):
    def notify(self, event: TileEvent):
        raise NotImplementedError(
            "TileListener subclass needs to override notify(TileEvent)")

class Listenable:
    """Objects to which listeners (like a view component) can be attached"""

    def __init__(self):
        self.listeners = [ ]

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)

    def notify_all(self, event: Event):
        for listener in self.listeners:
            listener.notify(event)

"""Classes for crucial parts of the model component (tile & board)"""

class Tile(Listenable):
    """One tile on the Sudoku grid.
    Public attributes (read-only): value, which will be either
    UNKNOWN or an element of CHOICES; candidates, which will
    be a set drawn from CHOICES.  If value is an element of
    CHOICES,then candidates will be the singleton containing
    value.  If candidates is empty, then no tile value can
    be consistent with other tile values in the grid.
    value is a public read-only attribute; change it
    only through the access method set_value or indirectly
    through method remove_candidates.
    """

    def __init__(self, row: int, col: int, value=UNKNOWN):
        """Assign position (row, col) and value (if specified) to this tile."""
        super().__init__()
        assert value == UNKNOWN or value in CHOICES
        self.row = row
        self.col = col
        self.set_value(value)

    def set_value(self, value: str):
        """Update tile's value and candidates from given value"""
        if value in CHOICES:
            self.value = value
            self.candidates = {value}
        else:
            self.value = UNKNOWN
            self.candidates = set(CHOICES)
        self.notify_all(TileEvent(self, EventKind.TileChanged))

    def __str__(self):
        """Return Tile value as string"""
        return str(self.value)

    def __repr__(self):
        """Return string like call to new Tile() object"""
        return f"Tile({self.row}, {self.col}, '{self.value}')"

    def could_be(self, value: str) -> bool:
        """True iff value is a candidate value for this tile"""
        return value in self.candidates
    
    def __hash__(self) -> int:
        """Hash on position only (not value)"""
        return hash((self.row, self.col))

    def remove_candidates(self, used_values: Set[str]) -> bool:
        """The used values cannot be a value of this unknown tile.
        We remove those possibilities from the list of candidates.
        If there is exactly one candidate left, we set the
        value of the tile.
        Returns:  True means we eliminated at least one candidate,
        False means nothing changed (none of the 'used_values' was
        in our candidates set).
        """
        new_candidates = self.candidates.difference(used_values)
        if new_candidates == self.candidates:
            # Didn't remove any candidates
            return False
        self.candidates = new_candidates
        if len(self.candidates) == 1:
            self.set_value(new_candidates.pop())
        self.notify_all(TileEvent(self, EventKind.TileChanged))
        return True

class Board(object):
    """A board has a matrix (list of lists) of Tile objects"""

    def __init__(self):
        """Initialize empty board (all Tiles UNKNOWN)"""
        # Each row contains columns (inner lists)
        self.tiles: List[List[Tile]] = []
        for row in range(NROWS):
            cols = []
            for col in range(NCOLS):
                cols.append(Tile(row, col))
            self.tiles.append(cols)
        self._form_groups()

    def _form_groups(self):
        """Create self.groups with groups for rows, cols, and blocks"""
        self.groups = []
        for row in self.tiles:
            self.groups.append(row)
        for col_num in range(len(self.tiles[0])):
            col_group = []
            for row in self.tiles:
                col_group.append(row[col_num])
            self.groups.append(col_group)
        for block_row in range(ROOT):
            for block_col in range(ROOT):
                group = [ ] 
                for row in range(ROOT):
                    for col in range(ROOT):
                        row_addr = (ROOT * block_row) + row
                        col_addr = (ROOT * block_col) + col
                        group.append(self.tiles[row_addr][col_addr])
                self.groups.append(group)

    def set_tiles(self, tile_values: Sequence[Sequence[str]]):
        """Set the tile values using a list of lists or list of strings"""
        for row_num in range(NROWS):
            for col_num in range(NCOLS):
                tile = self.tiles[row_num][col_num]
                tile.set_value(tile_values[row_num][col_num])

    def __str__(self) -> str:
        """In Sadman Sudoku format"""
        return "\n".join(self.as_list())


    def as_list(self) -> List[str]:
        """Tile values in a format compatible with set_tiles."""
        row_syms = [ ]
        for row in self.tiles:
            values = [tile.value for tile in row]
            row_syms.append("".join(values))
        return row_syms

    def is_consistent(self) -> bool:
        """Check that there are no duplicates within groups"""
        for group in self.groups:
            used = set()
            for tile in group:
                if tile.value in CHOICES:
                    # tile is not UNKNOWN
                    if tile.value in used:
                        # duplicate tile found
                        log.debug(f"Duplicate {tile.value} in {group}")
                        return False
                    else:
                        # new value, add to used
                        used.add(tile.value)
            # went through all groups without inconsistencies
        return True

    def solve(self):
        """General solver; guess-and-check 
        combined with constraint propagation.
        """
        self.propagate()
        if self.is_complete() and self.is_consistent():
            return True
        elif not self.is_consistent():
            return False
        else:
            state = self.as_list()
            tile = self.min_choice_tile()
            for value in tile.candidates:
                tile.set_value(value)
                if self.solve():
                    return True
                else:
                    self.set_tiles(state)
        # no possibilities worked
        return False
        
    def propagate(self):
        """Repeat solution tactics until we
        don't make any progress, whether or not
        the board is solved.
        """
        progress = True
        while progress:
            progress = self.naked_single()
            self.hidden_single()
        return

    def naked_single(self) -> bool:
        """Apply hidden single tactic for constraint propagation
        Eliminate candidates and check for sole remaining possibilities.
        Return value True means we crossed off at least one candidate.
        Return value False means we made no progress."""
        any_progress = False
        for group in self.groups:
            used_values = set([tile.value for tile in group])
            for tile in group:
                if tile.remove_candidates(used_values):
                    any_progress = True
        return any_progress

    def hidden_single(self) -> bool:
        """Apply hidden single tactic for constraint propagation"""
        any_progress = False
        for group in self.groups:
            unused_values = set(CHOICES).difference([tile.value for tile in group])
            for value in unused_values:
                occurrence = None
                for tile in group:
                    if value in tile.candidates:
                        if occurrence is None:
                            occurrence = tile
                        else:
                            occurrence = None
                            break
                if occurrence is not None:
                    occurrence.set_value(value)
                    any_progress = True
        return any_progress

    def min_choice_tile(self) -> Tile: 
        """Returns a tile with value UNKNOWN and 
        minimum number of candidates. 
        Precondition: There is at least one tile 
        with value UNKNOWN."""
        min_candidates = NROWS+1
        chosen_tile = None
        for row in self.tiles:
            for tile in row:
                if tile.value == UNKNOWN and len(tile.candidates) < min_candidates:
                    min_candidates = len(tile.candidates)
                    chosen_tile = tile
        assert isinstance(chosen_tile, Tile)
        return chosen_tile

    def is_complete(self) -> bool:
        """None of the tiles are UNKNOWN.  
        Note: Does not check consistency; do that 
        separately with is_consistent.
        """
        for row in self.tiles:
            for tile in row:
                if tile.value not in CHOICES:
                    return False
        return True