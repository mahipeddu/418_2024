import cv2
import numpy as np

def loadand_preprocess_image(image_path):
    """into blacckkk annd white """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _,binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return (binary_image // 255).astype(np.uint8), image

def find_edge_paths(grid):
    """fiding teh opening on top and bottotm edges , ie entrys and exita"""
    top_edge = grid[0, :]
    bottom_edge = grid[-1, :]
    start = (0, np.where(top_edge == 1)[0][0])
    end = (grid.shape[0] - 1, np.where(bottom_edge == 1)[0][0])
    return start, end

def find_neighbors(r, c, grid):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr][nc] == 1:
            neighbors.append((nr, nc))
    return neighbors

def bfs(grid, start, end):
    queue = [start]
    visited = set([start])
    parent = {start: None}
    t = 0
    traversed_nodes = set() 
    while queue:
        t+=1
        current = queue.pop(0)
        traversed_nodes.add(current) 
        if current == end:
            break
        for neighbor in find_neighbors(*current, grid):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    path.reverse()
    return path, t, len(traversed_nodes)

def draw_path_on_image(image, path):
    for i in range(len(path) - 1):
        start_point = (path[i][1], path[i][0])
        end_point = (path[i + 1][1], path[i + 1][0])
        image = cv2.line(image, start_point, end_point, (0, 255, 0), 2)
    return image

def solve_maze_and_draw_path(image_path,output_path):
    grid, original_image = loadand_preprocess_image(image_path)
    start, end = find_edge_paths(grid)
    path, dist,traversal = bfs(grid, start, end)

    if path:
        original_image_colored = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
        path_image = draw_path_on_image(original_image_colored, path)
        cv2.imwrite(output_path, path_image)
        print(f"The image with the path has been saved as '{output_path}'.")
        return traversal, dist




