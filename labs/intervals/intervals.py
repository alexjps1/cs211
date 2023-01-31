"""
Intervals Lab
by Alex JPS
CS 211
2023-01-11
"""

class Interval:
    """An interval m..n represents the set of intervals at least m and at most n."""
    def __init__(self, low: int, high: int):
        """Interval(low,high) is the interval low..high"""
        self.low = low
        self.high = high
        assert low < high, "Low must be lower than high"

    def contains(self, i: int) -> bool:
        """Integer i is within the closed interval"""
        if i in range(self.low, self.high + 1): 
            return True
        else:
            return False

    def overlaps(self, other: "Interval") -> bool: 
        """i.overlaps(j) iff i and j have some elements in common"""
        if self.high < other.low or self.low > other.high:
            return False
        else:
            return True

    def __eq__(self, other: "Interval") -> bool:
        """Interals are equal if they have the same low and high bounds"""
        if self.low == other.low and self.high == other.high:
            return True
        else:
            return False

    def join(self, other: "Interval") -> "Interval":
        """Create a new Interval that contains the union of elements in self and other.
        Precondition: self and other must overlap.
        """
        assert self.overlaps(other), "Intervals do not overlap"
        lowest = min(self.low, other.low)
        highest = max(self.high, other.high)
        return Interval(lowest, highest)

    def __str__(self):
        return f"[{self.low}..{self.high}]"

    def __repr__(self):
        return f"[{self.low}..{self.high}]"
