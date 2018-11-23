warehouse_floor = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
]


def neighbors(coord):

    [i, j] = coord

    # Potential neighbors are above, below, left, and right of coordinate
    neighbor_list = [[i, j + 1], [i, j - 1], [i + 1, j], [i - 1, j]]

    return neighbor_list


# Check if neighbors are valid. If out of bounds or -1, exclude from valid list.
def check_neighbors(warehouse_map, coord):
    neighbor_list = neighbors(coord)
    valid_neighbors = []
    bad_neighbors = []

    try:
        for [i, j] in neighbor_list:

            if i < 0 or j < 0:  # Exclude negative indexes. Negative indexes loop to end of list.
                bad_neighbors.append([i, j])
            elif warehouse_map[i][j] == 0:
                valid_neighbors.append([i, j])
            elif warehouse_map[i][j] == 1:
                bad_neighbors.append([i, j])

    except IndexError:  # If index error, then looking out of bounds of list
        bad_neighbors.append([i, j])

    return valid_neighbors


def is_traversable(warehouse_map, start_coord, end_coord):
    need_to_check = [start_coord]  # Initialize need to check with stating node
    checked_list = []

    # While need to check is not empty, keep looping
    while need_to_check:

        cur_coord = need_to_check.pop()  # Remove node from need_to_check
        valid_neighbors = check_neighbors(warehouse_map, cur_coord)  # Get valid neighbors from current node

        # Loop through valid neighbors of current node and see if its the end node
        for neighbor in valid_neighbors:

            if neighbor == end_coord:
                return True
            elif neighbor not in checked_list:  # In neighbor hasn't been checked previously, add to need_to_check
                need_to_check.append(neighbor)

        # Add current node to checked_list
        checked_list.append(cur_coord)

    # If need_to_check becomes empty, we have exhausted all coordinates we can get to and we haven't found end node
    return False


print(is_traversable(warehouse_floor, [0, 0], [3, 3]))