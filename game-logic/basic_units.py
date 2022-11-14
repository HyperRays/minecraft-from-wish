from dataclasses import dataclass
@dataclass(slots=True)
class vec2d:
    x: int
    y: int

    def __add__(self, other):
        return vec2d(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return vec2d(self.x-other.x, self.y-other.y)