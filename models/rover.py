DIRECTIONS = ['N', 'E', 'S', 'W']

# (x, y) deltas — N sobe (y-1), S desce (y+1), E direita (x+1), W esquerda (x-1)
DELTAS = {
    'N': (0, -1),
    'E': (1,  0),
    'S': (0,  1),
    'W': (-1, 0),
}


class Rover:
    def __init__(self, x=0, y=0, direction='N'):
        self.x = x
        self.y = y
        self.direction = direction

    def turn_left(self):
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx - 1) % 4]

    def turn_right(self):
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx + 1) % 4]

    def next_position(self, steps=1):
        dx, dy = DELTAS[self.direction]
        return self.x + dx * steps, self.y + dy * steps

    def prev_position(self, steps=1):
        dx, dy = DELTAS[self.direction]
        return self.x - dx * steps, self.y - dy * steps

    def to_dict(self):
        return {"x": self.x, "y": self.y, "dir": self.direction}
