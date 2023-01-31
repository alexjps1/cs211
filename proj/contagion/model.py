"""
Contagion Model
by Alex JPS
2023-01-30
CS 211
"""

import mvc # for Listenable
import enum
from typing import List, Tuple
import random
import config

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Health(enum.Enum):
    """Each individual is one discrete state of health"""
    vulnerable = enum.auto()
    asymptomatic = enum.auto()
    symptomatic = enum.auto()
    recovered = enum.auto()
    dead = enum.auto()

    def __str__(self) -> str:
        return self.name

class Population(mvc.Listenable):
    """Simple grid organization of individuals"""

    def __init__(self, nrows: int, ncols: int):
        """Create grid and fill with individuals based on config"""
        super().__init__()
        self.cells = []
        self.nrows = nrows
        self.ncols = ncols
        # Populate according to configuration
        for row_i in range(config.get_int("Grid", "Rows")):
            row = []
            for col_i in range(config.get_int("Grid", "Cols")):
                row.append(self._random_individual(row_i, col_i))
            self.cells.append(row)
        return

    def _random_individual(self, row: int, col: int) -> "Individual":
        """Return an individual type based on configured proportions"""
        classes = [(AtRisk, config.get_float("Grid", "Proportion_AtRisk")),
                   (Typical, config.get_float("Grid", "Proportion_Typical")),
                   (Wanderer, config.get_float("Grid", "Proportion_Wanderer"))]
        while True:
            for the_class, proportion in classes:
                dice = random.random()
                if dice < proportion:
                    return the_class(self, row, col)

    def step(self):
        """Calculate next state for all cells,
        then change all cells to new state"""
        log.debug("Population: Step")
        # Time passes
        for row in self.cells:
            for cell in row:
                cell.step()
        for row in self.cells:
            for cell in row:
                cell.tick()
        self.notify_all("timestep")

    def seed(self):
        """Infect a randomly-selected patient zero"""
        row = random.randint(0,self.nrows-1)
        col = random.randint(0,self.ncols-1)
        self.cells[row][col].infect()
        self.cells[row][col].tick()

    def count_in_state(self, state: Health) -> int:
        """Return how many individuals exist in a given health state"""
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.state == state:
                    count += 1
        return count

    def neighbors(self, num: int, row: int, col: int, dist: int) -> List[Tuple[int, int]]:
        """Return list of randomly-selected neighbors
        within a specfied Taxicab Distance of individual"""
        result = []
        count = 0
        log.debug(f"Cell {row},{col} finding {num} neighbors at distance {dist} " +
                  f"in {self.nrows},{self.ncols}")
        attempts = 0
        while count < num:
            attempts += 1
            assert attempts < 1000,(
                f"Can't find {num} neighbors at distance {dist}")
            row_step = random.randint(0-dist,dist)
            col_step = random.randint(0-dist,dist)
            row_addr = row + row_step
            col_addr = col + col_step
            # log.debug(f"Trying neighbor at position {row_addr},{col_addr}")
            if row_addr < 0 or row_addr >= self.nrows:
                # log.debug("Bad row")
                continue
            if col_addr < 0 or col_addr >= self.ncols:
                # log.debug("Bad column")
                continue
            if row_addr == row and col_addr == 0:
                # log.debug("Can't visit self")
                continue
            neighbor_addr = (row_addr, col_addr)
            if neighbor_addr in result:
                continue
            log.debug(f"{row},{col} adding neighbor at {row_addr},{col_addr}")
            result.append(neighbor_addr)
            count += 1
        return result

    def visit(self, address: Tuple[int, int]):
        """Return Invidiual object associated with given address"""
        row_num, col_num = address
        return self.cells[row_num][col_num]

class Individual(mvc.Listenable):
    """Abstract class for an individual in the population.
    Individuals will also inherit from one of the abstract classes."""

    def __init__(self, kind: str, region: Population, row: int, col: int):
        """Set variables according to configuration for specified kind (subclass) of individual"""
        # Listener needs its own initialization
        super().__init__()
        self.kind = kind
        self.region = region
        self.row = row
        self.col = col
        # Initially we are 'vulnerable', not yet infected
        self._time_in_state = 0  # How long in this state?
        self.state = Health.vulnerable
        self.next_state = Health.vulnerable
        # Configuration parameters based on kind
        self.T_Incubate = config.get_int(kind, "T_Incubate")
        self.P_Transmit = config.get_float(kind, "P_Transmit")
        self.T_Recover = config.get_int(kind, "T_Recover")
        self.P_Death = config.get_float(kind, "P_Death")
        self.P_Greet = config.get_float(kind, "P_Greet")
        self.N_Neighbors = config.get_int(kind, "N_Neighbors")
        self.P_Visit = config.get_float(kind, "P_Visit")
        self.Visit_Dist = config.get_int(kind, "Visit_Dist")
        # Define own neighbors using Population.neighbors() method
        self.neighbors = region.neighbors(num=self.N_Neighbors,
                                          row=row, col=col,
                                          dist=self.Visit_Dist)

    def infect(self):
        """Become asymptomatic when called by another individual
        or patient zero seed()"""
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic
    
    def step(self):
        """Calculate Individual's next state of health"""
        # Basic state transitions are in common
        if self.state == Health.asymptomatic:
            if self._time_in_state > self.T_Incubate:
                self.next_state = Health.symptomatic
                log.debug("Becoming symptomatic")
        if self.state == Health.symptomatic:
            # We could die on any time step before we recover
            if self._time_in_state > self.T_Recover:
                log.debug(f"Recovery at {self.row},{self.col}")
                self.next_state = Health.recovered
            elif random.random() < self.P_Death:
                log.debug(f"Death at {self.row},{self.col}")
                self.next_state = Health.dead
        # Social behavior differs among concrete classes
        self.social_behavior()

    def tick(self):
        """Calculate time in current health state and progress to next state"""
        self._time_in_state += 1
        if self.state != self.next_state:
            self.state = self.next_state
            self.notify_all("newstate")
            # Reset clock
            self._time_in_state = 0

    def social_behavior(self):
        raise NotImplementedError("Social behavior should be implemented in subclasses")

    def meet(self, other: "Individual"):
        """Possibly inflect individuals who are meeting"""
        self.maybe_transmit(other)  # I might infect you
        other.maybe_transmit(self)  # You might infect me

    def maybe_transmit(self, other: "Individual"):
        """If infection is possible during a visist,
        randomly decide whether to infect."""
        if not self._is_contagious():
            return
        if not other.state == Health.vulnerable:
            return
        # Transmission is possible.  Roll the dice
        if random.random() < self.P_Transmit:
            other.infect()

    def _is_contagious(self) -> bool:
        """SARS COVID 19 apparently spreads before the individual is symptomatic."""
        # return true if individual infected, even asymptomatic
        return (self.state == Health.symptomatic or self.state == Health.asymptomatic)

    def hello(self, visitor: "Individual") -> bool:
        """True for 'welcome in' and False for 'go away'"""
        raise NotImplementedError("Cannot call hello() method from abstract Individual class")

class Typical(Individual):
    """Typical individual may visit different neighbors each day."""
    def __init__(self, region: Population, row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("Typical", region, row, col)

    def hello(self, visitor: "Individual") -> bool:
        """Typical individual almost always accepts a visit"""
        if random.random() <= self.P_Greet:
            return True
        return False

    def social_behavior(self):
        """A typical individual visits neighbors at random"""
        if random.random() < self.P_Visit:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            if neighbor.hello(self):
                neighbor.meet(self)

class AtRisk(Individual):
    """Immunocompromised or elderly individuals,
    vunerable and cautious"""
    def __init__(self, region: "Population", row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("AtRisk", region, row, col)
        # AtRisk individual will keep in mind who they visit
        self.prior_visit = None

    def hello(self, visitor: "Individual"):
        """AtRisk individual only accepts visits from own neighbors"""
        visitor_pos = (visitor.row, visitor.col)
        if visitor_pos in self.neighbors:
            return True
        else:
            return False

    def social_behavior(self):
        """AtRisk individual tries to visit same neighbors twice"""
        if random.random() >= self.P_Visit:
            # No visits today! 
            return
        if self.prior_visit is None:
            # Time for someone new
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            self.prior_visit = neighbor
        else:
            # Second visit to the same person
            neighbor = self.prior_visit
            self.prior_visit = None
        if neighbor.hello(self):
            neighbor.meet(self)

class Wanderer(Individual):
    """Individual who visits neighbors frequently and across a longer distance"""
    def __init__(self, region: Population, row: int, col: int):
        # Much of the constructor has been "factored out" into
        # the abstract base class
        super().__init__("Wanderer", region, row, col)

    def hello(self, visitor: "Individual") -> bool:
        """Wanderer individual always accepts a visit"""
        if random.random() <= self.P_Greet:
            return True
        return False

    def social_behavior(self):
        """A Wanderer visits many neighbors at random"""
        if random.random() < self.P_Visit:
            addr = random.choice(self.neighbors)
            neighbor = self.region.visit(addr)
            if neighbor.hello(self):
                neighbor.meet(self)