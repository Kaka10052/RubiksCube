import numpy as np


class Piece:
    def __init__(self, parts):
        self.parts = parts
        if isinstance(self.parts, np.ndarray):
            self.n_parts = len(parts.flatten())
            self.wall_names = [part.wall_name for part in self.parts.flatten()]
        else:
            self.n_parts = len(parts)
            self.wall_names = [part.wall_name for part in self.parts]

    def __repr__(self):
        return str(self.parts)

    def contains_wall(self, wall_name):
        return wall_name in self.wall_names

    def move(self, move):
        border_parts = [part for part in self.parts if part.wall_name != move.wall]
        new_walls_dict = move.get_new_walls_dict()
        for part in border_parts:
            part.wall_name = new_walls_dict[part.wall_name]


