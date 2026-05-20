DIRECTIONS = ['N', 'E', 'S', 'W']

# (x, y) por direção — y=0 é o topo, por isso N = (0, -1)
DELTAS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}


# Representa o estado do rover: posição (x, y) e direção
class Rover:
    def __init__(self, x=0, y=0, direction='N'):
        self.x = x
        self.y = y
        self.direction = direction

    # Gira 90° para a esquerda
    def turn_left(self):
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx - 1) % 4]

    # Gira 90° para a direita
    def turn_right(self):
        idx = DIRECTIONS.index(self.direction)
        self.direction = DIRECTIONS[(idx + 1) % 4]

    # Retorna a posição (x, y) N células à frente sem mover o rover
    def next_position(self, steps=1):
        dx, dy = DELTAS[self.direction]
        return self.x + dx * steps, self.y + dy * steps

    # Retorna a posição (x, y) N células atrás sem mover o rover
    def prev_position(self, steps=1):
        dx, dy = DELTAS[self.direction]
        return self.x - dx * steps, self.y - dy * steps

    # Serializa o estado do rover para JSON
    def to_dict(self):
        return {"x": self.x, "y": self.y, "dir": self.direction}
