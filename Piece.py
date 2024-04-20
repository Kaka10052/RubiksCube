import numpy as np

import constants


class Piece:
    def __init__(self, parts):
        self.parts = parts
        if not isinstance(self.parts, np.ndarray):
            self.parts = np.array(parts)
        self.n_parts = len(self.parts.flatten())
        self.wall_names = [part.wall_name for part in self.parts.flatten()]

    def __repr__(self):
        return str(self.parts)

    def contains_wall(self, wall_name):
        return wall_name in self.wall_names

    def move(self, move):
        border_parts = [part for part in self.parts if part.wall_name != move.wall_name]
        new_walls_dict = move.get_new_walls_dict()
        for part in border_parts:
            letter = constants.wall2letter[part.wall_name]
            to_wall = constants.letter2wall[new_walls_dict[letter]]
            part.wall_name = to_wall


