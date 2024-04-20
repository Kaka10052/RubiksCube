from turtle import back

from Move import Move
from Part import Part
from Piece import Piece
from Wall import Wall
import numpy as np
import constants as const
from constants import set_correct_wall_names, walls_to_colors
from extra import CircularLinkedList
from typing import cast
# TODO Create class with constants?


class Cube:
    def __init__(self, dim):
        self.dim = dim
        self.centers = []
        self.edges = []
        self.corners = []
        self.walls = []
        self.build_cube()
        self.pieces = zip(self.centers, self.edges, self.corners)
        self.is_correct()

    def is_correct(self):
        # TODO add is_correct() method that checks if there is proper number of walls, edges, corners etc.
        if self.dim <= 1:
            raise Exception("Number of dimensions should be greater than 1")

        correct_num_walls = 6
        wrong_num_walls = len(self.walls) != correct_num_walls
        wrong_num_edges = len(self.edges) != 12 * (self.dim-2)
        wrong_num_corners = len(self.corners) != 8
        wrong_num_centers = len(self.centers) != correct_num_walls * (self.dim-2) ** 2
        wrong_num = [wrong_num_centers, wrong_num_corners, wrong_num_edges, wrong_num_walls]
        if any(wrong_num):
            raise Exception("Wrong number of pieces")

        cube_wall_names = [wall.name for wall in self.walls]
        if set_correct_wall_names != set(cube_wall_names):
            raise Exception("Wrong wall names. Check if wall names are not duplicated.")

    def build_cube(self):
        self.build_walls()
        self.build_centers()
        self.build_edges()
        self.build_corners()
        self.is_correct()

    def build_walls(self):
        walls = []
        for wall_name in set_correct_wall_names:
            color = walls_to_colors[wall_name]
            wall_pieces = [[Part(color, wall_name) for _ in range(self.dim)] for _ in range(self.dim)]
            wall = Wall(np.array(wall_pieces), wall_name, self.dim)
            walls.append(wall)
        self.walls = walls

    def build_centers(self):
        centers_grid = np.array([wall.parts[1:self.dim - 1, 1:self.dim - 1] for wall in self.walls])
        self.centers = [Piece([center]) for center in centers_grid.flatten()]

    def get_walls_order(self, wall_name, num_rotation=0):
        letters_order = const.wall_lists[wall_name]
        if num_rotation:
            cll_walls_order = CircularLinkedList(letters_order)
            cll_walls_order.rotate_right(num_rotation)
            letters_order = cll_walls_order.to_list()
        walls_order = [const.letter2wall[letter] for letter in letters_order]
        return walls_order

    def build_edges(self):
        edges = []
        front_edges = self.build_edges_front()
        back_edges = self.build_edges_back()
        mid_edges = self.build_edges_mid()
        edges.extend(front_edges)
        edges.extend(mid_edges)
        edges.extend(back_edges)

        self.edges = edges

    def build_edges_front(self):
        # Difference between this method and build_edges_back is front_wall and different external_side_order
        # Although I need to be more descriptive about those orders and what I would like to do with them
        front_wall = self.find_wall(const.FRONT_WALL)
        inner_sides_order = self.get_walls_order(const.FRONT_WALL)
        external_walls_order = inner_sides_order
        external_edges = self.get_external_edges(external_walls_order)
        inner_edges = front_wall.get_inner_edges_parts(side_order=inner_sides_order)
        front_edges = self.connect_edges(external_edges, inner_edges)
        return front_edges

    def build_edges_back(self):
        back_wall = self.find_wall(const.BACK_WALL)
        inner_sides_order = self.get_walls_order(const.FRONT_WALL)
        external_walls_order = self.get_walls_order(const.BACK_WALL)
        external_edges = self.get_external_edges(external_walls_order)
        inner_edges = back_wall.get_inner_edges_parts(side_order=inner_sides_order)
        back_edges = self.connect_edges(external_edges, inner_edges)
        return back_edges

    def build_edges_mid(self):
        mid_edges = []

        up_wall = self.find_wall(const.UP_WALL)
        down_wall = self.find_wall(const.DOWN_WALL)
        right_wall = self.find_wall(const.RIGHT_WALL)
        left_wall = self.find_wall(const.LEFT_WALL)
        up_right_side = up_wall.get_side_edges(const.RIGHT_WALL)
        up_left_side = up_wall.get_side_edges(const.LEFT_WALL)
        down_right_side = down_wall.get_side_edges(const.RIGHT_WALL)
        down_left_side = down_wall.get_side_edges(const.LEFT_WALL)
        right_up_side = right_wall.get_side_edges(const.LEFT_WALL)
        right_down_side = right_wall.get_side_edges(const.LEFT_WALL)
        left_up_side = left_wall.get_side_edges(const.LEFT_WALL)
        left_down_side = left_wall.get_side_edges(const.LEFT_WALL)
        mid_edges.extend(self.connect_edges(up_right_side, right_up_side))
        mid_edges.extend(self.connect_edges(up_left_side, left_up_side))
        mid_edges.extend(self.connect_edges(down_right_side, right_down_side))
        mid_edges.extend(self.connect_edges(down_left_side, left_down_side))

        return mid_edges

    def connect_edges(self, external_edges, inner_edges):
        connected_edges = [Piece([inner_edge, external_edge])
                       for inner_edge, external_edge in zip(inner_edges, external_edges)]
        return connected_edges

    def get_external_edges(self, external_walls_order):
        external_sides_order = self.get_walls_order(const.FRONT_WALL, num_rotation=2)
        external_edges = []
        for wall_name, side in zip(external_walls_order, external_sides_order):
            wall = self.find_wall(wall_name)
            edges = wall.get_side_edges(side)
            for edge in edges:
                external_edges.append(edge)
        return external_edges

    def build_corners(self):
        front_wall = self.find_wall(const.FRONT_WALL)
        back_wall = self.find_wall(const.BACK_WALL)
        left_wall = self.find_wall(const.LEFT_WALL)
        right_wall = self.find_wall(const.RIGHT_WALL)
        up_wall = self.find_wall(const.UP_WALL)
        down_wall = self.find_wall(const.DOWN_WALL)
        white_green_blue = Piece([up_wall.parts[-1, -1], front_wall.parts[0, -1], right_wall.parts[0, 0]])
        white_green_orange = Piece([up_wall.parts[-1, 0], front_wall.parts[0, 0], left_wall.parts[0, -1]])
        white_blue_orange = Piece([up_wall.parts[0, 0], back_wall.parts[-1, 0], left_wall.parts[0, 0]])
        white_blue_red = Piece([up_wall.parts[0, -1], back_wall.parts[-1, -1], right_wall.parts[0, -1]])
        yellow_green_orange = Piece([down_wall.parts[0, 0], front_wall.parts[-1, 0], left_wall.parts[-1, -1]])
        yellow_green_red = Piece([down_wall.parts[0, -1], front_wall.parts[-1, -1], right_wall.parts[-1, 0]])
        yellow_blue_orange = Piece([down_wall.parts[-1, 0], back_wall.parts[0, 0], left_wall.parts[-1, 0]])
        yellow_blue_red = Piece([down_wall.parts[-1, -1], back_wall.parts[0, -1], right_wall.parts[-1, -1]])
        corners = [white_green_blue, white_green_orange, white_blue_orange, white_blue_red,
                   yellow_green_orange, yellow_green_red, yellow_blue_orange, yellow_blue_red]

        self.corners = corners

    def find_wall(self, wall_name) -> Wall:
        for wall in self.walls:
            if wall.name == wall_name:
                return wall

    def move(self, notation):
        move = Move(notation)
        wall_to_move = self.find_wall(move.wall_name)
        wall_to_move.rotate(move)
        all_pieces = self.corners.copy()
        all_pieces.extend(self.edges)
        all_pieces.extend(self.corners)

        pieces_to_move = [piece for piece in all_pieces if piece.contains_wall(move.wall_name)]
        for piece in pieces_to_move:
            piece.move(move)



