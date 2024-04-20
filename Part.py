class Part:
    def __init__(self, color, wall_name, wall_cords):
        self.color = color
        self.wall_name = wall_name
        self.wall_cords = wall_cords

    def __str__(self):
        return f'Part\'{self.color}\', \'{self.wall_name}\', {self.wall_cords})'

    def __repr__(self):
        return f'Part(\'{self.color}\', \'{self.wall_name}\', {self.wall_cords})'










