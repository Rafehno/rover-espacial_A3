# Representa o terreno 2D onde o rover se move
class Grid:
    def __init__(self, width=10, height=10, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(map(tuple, obstacles)) if obstacles else set()

    # Verifica se a célula (x, y) está dentro dos limites do grid
    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # Verifica se há um obstáculo na célula (x, y)
    def has_obstacle(self, x, y):
        return (x, y) in self.obstacles

    # Retorna True se o rover não pode entrar na célula (fora do grid ou obstáculo)
    def is_blocked(self, x, y):
        return not self.is_valid(x, y) or self.has_obstacle(x, y)

    # Serializa o grid para JSON
    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "obstacles": [list(o) for o in self.obstacles],
        }
