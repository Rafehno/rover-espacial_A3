class Grid:
    def __init__(self, width=10, height=10, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(map(tuple, obstacles)) if obstacles else set()

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def has_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def is_blocked(self, x, y):
        return not self.is_valid(x, y) or self.has_obstacle(x, y)

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "obstacles": [list(o) for o in self.obstacles],
        }
