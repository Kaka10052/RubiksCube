from extra import CircularLinkedList
from constants import wall_lists, letter2wall, correct_letters


class Move:
    def __init__(self, notation):
        self.notation = notation
        self.wall_name = ''
        self.num_rotations = 1
        self.is_reverse = False
        self.decode_notation()

    def decode_notation(self):
        letter = self.notation[0].upper()
        try:
            self.wall_name = letter2wall[letter]
        except KeyError:
            raise Exception("Wrong letter. Please make sure letter is in the list: " + str(correct_letters))

        if len(self.notation) == 1:
            return
        if self.notation[1].isnumeric():
            self.num_rotations = 2
        elif self.notation[1] == "'":
            self.is_reverse = True
        else:
            raise Exception("Incorrect notation. Please check it again.")

    def get_new_walls_dict(self):
        """It creates a new dictionary that maps old wall names to their corresponding new wall names
        based on rotations performed on a circular linked list of walls"""
        new_walls_cll = CircularLinkedList(wall_lists[self.wall_name])
        if self.is_reverse:
            new_walls_cll.rotate_right(self.num_rotations)
        else:
            new_walls_cll.rotate_left(self.num_rotations)
        new_walls = new_walls_cll.to_list()
        old_walls = wall_lists[self.wall_name]
        new_walls_dict = {old_wall: new_wall for old_wall, new_wall in zip(old_walls, new_walls)}
        return new_walls_dict


