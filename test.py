import math

def explore_map(map, start_x, start_y, angle):
    """
    Explores a 2D map in a straight line from a given starting point and angle.

    Args:
        map: A 2D list representing the map.
        start_x: The x-coordinate of the starting point.
        start_y: The y-coordinate of the starting point.
        angle: The angle of exploration in degrees.

    Returns:
        The final position after exploration.
    """

    height = len(map)
    width = len(map[0])

    # Convert angle to radians
    angle_rad = angle * (math.pi / 180)

    # Calculate the step size in x and y directions
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    x, y = start_x, start_y

    while 0 <= x < width and 0 <= y < height and map[y][x] == 0:
        map[y][x] = 1
        x += dx
        y += dy
        x = int(round(x))
        y = int(round(y))

    return x, y


map = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

start_x, start_y = 0, 0
angle = 45

final_x, final_y = explore_map(map, start_x, start_y, angle)

print(final_x,final_y)