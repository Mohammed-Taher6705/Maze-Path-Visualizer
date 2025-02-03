from PIL import Image, ImageDraw # type: ignore
import heapq
import random
import pygame

# Heuristic Function (Manhattan distance)
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# A* Algorithm
def a_star(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_score[goal]
                
        for neighbor, _, cost in graph[current]:
            tentative_g_score = g_score[current] + cost
            neighbor = (neighbor,_)

            if tentative_g_score < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if (f_score[neighbor], neighbor) not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
    return None, float('inf')

# Reconstruct Path
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# Maze Creation
def create_maze(width, height, obstacle_percentage=0.2, weighted_percentage=0.1, seed=42):
    random.seed(seed)
    maze = []
    for i in range(height):
        row = []
        for j in range(width):
            if random.random() < obstacle_percentage:
                row.append('#')
            else:
                if random.random() < weighted_percentage:
                    row.append(random.randint(2, 5))
                else:
                    row.append(1)
        maze.append(row)
    return maze

# Print Maze for Visual Debugging
def print_maze(maze):
    for row in maze:
        print(' '.join(str(cell) for cell in row))

# Get Neighbors
def get_neighbors(x, y, maze):
    neighbors = []
    height = len(maze)
    width = len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] != '#':
            neighbors.append((nx, ny, maze[ny][nx]))
    return neighbors

# Create Graph
def create_graph(maze):
    graph = {}
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] != '#':
                graph[(x, y)] = get_neighbors(x, y, maze)
    return graph

# GIF Creation
def create_visual_frames(maze, path, save_path="maze_path.gif"):
    cell_size = 10
    frames = []
    for i in range(len(path)):
        frame = Image.new("RGB", (len(maze[0]) * cell_size, len(maze) * cell_size), "white")
        draw = ImageDraw.Draw(frame)

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                color = "black" if cell == "#" else "white"
                draw.rectangle(
                    [x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size],
                    fill=color
                )

        for j in range(i + 1):
            x, y = path[j]
            draw.rectangle(
                [x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size],
                fill="blue"
            )

        start_x, start_y = path[0]
        goal_x, goal_y = path[-1]
        draw.rectangle(
            [start_x * cell_size, start_y * cell_size, (start_x + 1) * cell_size, (start_y + 1) * cell_size],
            fill="green"
        )
        draw.rectangle(
            [goal_x * cell_size, goal_y * cell_size, (goal_x + 1) * cell_size, (goal_y + 1) * cell_size],
            fill="red"
        )

        frames.append(frame)

    frames[0].save(save_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
    print(f"GIF saved at {save_path}")

# Example Execution
maze = create_maze(50, 50)
graph = create_graph(maze)
start = (0, 0)
goal = (49, 49)

if goal not in graph:
    print("Goal is unreachable due to obstacles.")
else:
    path, cost = a_star(graph, start, goal)
    if path:
        print("Path found with cost:", cost)
        create_visual_frames(maze, path)
    else:
        print("Path not found.")
