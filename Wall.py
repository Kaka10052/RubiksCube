import numpy as np
from Piece import Piece
from Part import Part
import constants as const
from Move import Move

class Wall:
    def __init__(self, parts, name, dimension):
        self.parts: np.array() = parts
        self.name = name
        self.dim = dimension
        self.is_correct()

    def __repr__(self):
        return f'Wall({self.parts})'

    def is_correct(self):
        # TODO consider making this method more general and adding to Piece
        wall_piece = Piece(self.parts)
        wrong_n_parts = wall_piece.n_parts != self.dim**2
        set_wall_names = set(wall_piece.get_wall_names())
        wrong_wall_name = len(set_wall_names) != 1 and self.name not in set_wall_names
        wrong_data = wrong_n_parts or wrong_wall_name

        if wrong_data:
            err_msg = f"Wrong data. Check if number of parts is {self.dim**2} " \
                      f"or all the pieces have the same wall name as {self.name}"
            raise Exception(err_msg)

    def update_parts_cords(self):
        for row_i in range(self.dim):
            for col_i in range(self.dim):
                part_to_rotate: Part = self.parts[row_i, col_i]
                part_to_rotate.wall_cords = (row_i, col_i)
    def rotate(self, move: Move):
        axes = (1, 0) if not move.is_reverse else (0, 1)
        self.parts = np.rot90(self.parts, move.num_rotations, axes=axes)
        self.update_parts_cords()

    def get_correct_wall_name(self, name_to_check):
        name_to_check = name_to_check.upper()
        correct_letters = const.wall_lists[const.FRONT_WALL]
        correct_walls = [const.letter2wall[letter] for letter in correct_letters]
        correct_strings = correct_walls + correct_letters
        if name_to_check not in correct_strings:
            raise Exception("Incorrect wall name")
        is_letter = name_to_check in const.correct_letters
        wall_name = const.letter2wall[name_to_check] if is_letter else name_to_check
        return wall_name

    def get_side_edges(self, side_name):
        edges = []
        if self.dim == 2:
            return edges
        side_name = self.get_correct_wall_name(side_name)

        if side_name == const.UP_WALL:
            return list(self.parts[0, 1:-1])
        if side_name == const.RIGHT_WALL:
            return list(self.parts[1:-1, -1])
        if side_name == const.DOWN_WALL:
            return list(self.parts[-1, 1:-1])
        if side_name == const.LEFT_WALL:
            return list(self.parts[1:-1, 0])
        else:
            raise Exception("Got incorrect wall name")

    def get_inner_edges_parts(self, side_order=const.wall_lists[const.FRONT_WALL]):
        return [edge for side in side_order for edge in self.get_side_edges(side)]

    def get_corners(self):
        return [self.parts[x, y] for x in (0, -1) for y in (0, -1)]

    def get_segment_to_replace(self):
        for i in (0, -1):
            segments = [self.parts[i, :].flatten(), self.parts[:, i].flatten()]
            for segment in segments:
                wall_names = set(part.wall_name for part in segment)
                if len(wall_names) == 1 and wall_names.pop() != self.name:
                    return segment
        print("All segments are correct")
        return

    def replace_segment(self, new_segment):
        for i in (0, -1):
            # replace row
            segment = self.parts[i, :]
            wall_names = set(part.wall_name for part in segment)
            if len(wall_names) == 1 and wall_names.pop() != self.name:
                self.parts[i, :] = new_segment
                break
            # replace column
            segment = self.parts[:, i]
            wall_names = set(part.wall_name for part in segment)
            if len(wall_names) == 1 and wall_names.pop() != self.name:
                self.parts[:, i] = new_segment
                break
