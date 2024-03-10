from Cube import Cube

cube = Cube(3)
cube.build_walls()
cube.build_edges()
cube.walls[0].get_inner_edges_parts()
