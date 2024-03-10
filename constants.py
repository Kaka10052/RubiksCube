# Walls
LEFT_WALL = 'LEFT'
RIGHT_WALL = 'RIGHT'
UP_WALL = 'UP'
DOWN_WALL = 'DOWN'
FRONT_WALL = 'FRONT'
BACK_WALL = 'BACK'
set_correct_wall_names = {LEFT_WALL, RIGHT_WALL, UP_WALL, DOWN_WALL, FRONT_WALL, BACK_WALL}
wall_lists = {
    FRONT_WALL: ['U', 'R', 'D', 'L'],
    BACK_WALL:  ['U', 'L', 'D', 'R'],
    UP_WALL:    ['F', 'L', 'B', 'R'],
    DOWN_WALL:  ['F', 'R', 'B', 'L'],
    LEFT_WALL:  ['F', 'D', 'B', 'U'],
    RIGHT_WALL: ['F', 'U', 'B', 'D']
}
walls_to_colors = {
    FRONT_WALL: 'green',
    BACK_WALL:  'blue',
    UP_WALL:    'white',
    DOWN_WALL:  'yellow',
    LEFT_WALL:  'orange',
    RIGHT_WALL: 'red'
}
opposite_walls = {
    FRONT_WALL: BACK_WALL,
    BACK_WALL: FRONT_WALL,
    UP_WALL: DOWN_WALL,
    DOWN_WALL: UP_WALL,
    LEFT_WALL: RIGHT_WALL,
    RIGHT_WALL: LEFT_WALL
}

# Letters
correct_letters = ['F', 'B', 'U', 'D', 'R', 'L']
letter2wall = {
    'F': FRONT_WALL,
    'B': BACK_WALL,
    'U': UP_WALL,
    'D': DOWN_WALL,
    'R': RIGHT_WALL,
    'L': LEFT_WALL
}
