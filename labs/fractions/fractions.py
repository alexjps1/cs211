"""
fractions.py
by Alex JPS
2021-01-18
CS 211
"""

def gcd(a, b) -> int:
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

class Fraction:
    
    def __init__(self, num, den):
        self.num = int(num)
        self.den = int(den)
        assert den > 0, "No negative denominators"
        assert num > 0, "No negative numerators"
        assert not den == 0, "No zero denominators"
        self.simplify()
        
    def __str__(self) -> str:
        self.num = int(self.num)
        self.den = int(self.den)
        return f"{self.num}/{self.den}"
    
    def __repr__(self) -> str:
        self.num = int(self.num)
        self.den = int(self.den)
        return f"Fraction({self.num},{self.den})"

    def __mul__(self, other: "Fraction") -> "Fraction":
        result = Fraction(self.num * other.num, self.den * other.den)
        result.simplify()
        return result
    
    def __add__(self, other: "Fraction") -> "Fraction":
        result = Fraction(self.num * other.den + other.num * self.den, self.den * other.den)
        result.simplify()
        return result

    def simplify(self):
        common_div = gcd(self.num, self.den)
        self.num = self.num / common_div
        self.den = self.den / common_div
