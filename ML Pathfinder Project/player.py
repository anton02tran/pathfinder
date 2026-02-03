#  FUNCTION TO FIND VALID NEIGHBOURS OF A PATHFINDER

def get_neighbors(pos, grid, ROWS, COLS): 

    neighbours = []
    r, c = pos

    # DEFINE DIRECTIONS, U D L R
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_r, new_c = r + dr, c + dc

        # BOUNDARY CHECK
        if 0 <= new_r < ROWS and 0 <= new_c < COLS:
            # WALL/OBSTACLE CHECK
            if grid[new_r][new_c] not in [1, 4]:
                neighbours.append((new_r, new_c))

    return neighbours

# BREADTH-FIRST SEARCH FUNCTION

from collections import deque

def bfs(start, end, grid, rows, cols):
    # QUEUE VALUES (current_position, path_taken)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()
        
        # CHECK IF ENDED
        if current == end:
            return path

        # CHECK NEIGHBOURS
        for neighbor in get_neighbors(current, grid, rows, cols):
            if neighbor not in visited:
                visited.add(neighbor)
                # CREAT NEW PATH BY ADDING VALUE TO OLD PATH
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
    
    return None # No path found