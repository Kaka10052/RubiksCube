class Part:
    def __init__(self, color, wall_name):
        self.color = color
        self.wall_name = wall_name

    def __str__(self):
        return f'Part\'{self.color}\', \'{self.wall_name}\')'

    def __repr__(self):
        return f'Part(\'{self.color}\', \'{self.wall_name}\')'










