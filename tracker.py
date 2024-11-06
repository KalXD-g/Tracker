import random
import time
import sys
sys.setrecursionlimit(2000)  # Set a new limit


# * CREATES THE MAZE. [AI GENERATED]
def generate_maze(width, height, obstacle_percentage):
    # Create a maze filled with zeros (paths)
    maze = [[0 for _ in range(width)] for _ in range(height)]

    # Set start and end points
    start_point = (0, 0)
    end_point = (height - 1, width - 1)

    # Randomly place obstacles based on the specified percentage
    total_cells = width * height
    num_obstacles = int(total_cells * (obstacle_percentage / 100))

    # Ensure that the start and end points are not blocked
    while num_obstacles > 0:
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        if (x, y) != start_point and (x, y) != end_point and maze[x][y] == 0:
            maze[x][y] = 1  # Place an obstacle
            num_obstacles -= 1

    # Ensure the maze is solvable by removing obstacles along a path
    # Create a simple path from start to end
    current_position = start_point
    while current_position != end_point:
        maze[current_position[0]][current_position[1]] = 0  # Clear the path
        if current_position[0] < end_point[0]:
            current_position = (current_position[0] + 1, current_position[1])  # Move down
        elif current_position[1] < end_point[1]:
            current_position = (current_position[0], current_position[1] + 1)  # Move right

    return maze


# * DOES AN INITIAL CHECK WHETHER THE MAZE IS SOLVABLE OR NOT
def initialMazeCheck(maze, start_point, goal):
    # Checks if start and goal points are clear
    if (maze[0][1] == 0 or maze[1][0] == 0) and (maze[-2][-1] == 0 or maze[-1][-2] == 0) and maze[start_point[0]][start_point[1]] == 0 and maze[goal[0]][goal[1]] == 0:
        return True  # Path is clear

    # Checks for blockage at the start point
    if maze[0][1] == 1 and maze[1][0] == 1:
        print("Start point is being blocked")
        return False  # Start point blocked

    # Checks for blockage at the goal point
    elif maze[-2][-1] == 1 and maze[-1][-2] == 1:
        print("Goal point is being blocked")
        return False  # Goal point blocked

    return None  # Returns None if no conditions are met


# * CREATES A TRACKER
points_visited_sttracker = []  # holds the points visited by tracker from the start point
points_visited_bktracker = []  # stores the points from back tracker

def tracker(maze, position, points_visited_bktracker, points_visited_sttracker):
    x, y = position

    # checks if the position is valid
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]) or maze[x][y] != 0:
        return None
    
    maze[x][y] = 2  # Marks as visited
    if position in points_visited_bktracker:
        print("Maze solved")
        return True
    else:
        points_visited_sttracker.append(position)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    valid_moves = []  # to store valid next moves

    for direction in directions:
        new_position = (x + direction[0], y + direction[1])

        # Checks if the next point is valid and not already visited
        if (0 <= new_position[0] < len(maze) and 0 <= new_position[1] < len(maze[0]) and maze[new_position[0]][new_position[1]] == 0):
            valid_moves.append(new_position)  # collects all the valid moves

    for next_position in valid_moves:
        if tracker(maze, next_position, points_visited_sttracker, points_visited_bktracker):  # New tracker for each valid path
            return True

    return False  # Return False if no paths lead to the goal


# * CREATES A BACK TRACKER
def backtracker(maze, position, points_visited_sttracker, points_visited_bktracker):
    xi, yi = position

    if xi < 0 or yi < 0 or xi >= len(maze) or yi >= len(maze[0]) or maze[xi][yi] != 0:
        return None
    
    maze[xi][yi] = 2  # Marks as visited

    if position in points_visited_sttracker:
        print("Maze solved")
        return True
    else:
        points_visited_bktracker.append(position)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    valid_moves = []  # to store valid next moves

    for direction in directions:
        new_position = (xi + direction[0], yi + direction[1])

        # Checks if the next point is valid and not already visited
        if (0 <= new_position[0] < len(maze) and 0 <= new_position[1] < len(maze[0]) and maze[new_position[0]][new_position[1]] == 0):
            valid_moves.append(new_position)  # collects all the valid moves

    for next_position in valid_moves:
        if backtracker(maze, next_position, points_visited_sttracker, points_visited_bktracker):  # New backtracker for each valid path
            return True

    return False  # Return False if no paths lead to the goal


# * MAIN FUNCTION
# Set parameters
width, height = 50, 50
obstacle_percentage = 30  # Adjust this percentage for more or fewer obstacles

# Generate the maze
maze = generate_maze(width, height, obstacle_percentage)

# Print the maze in 2D matrix format
for row in maze:
    print(row)

start_point = (0, 0)
goal = (49, 49)

if initialMazeCheck(maze, start_point, goal):
    start_time = time.time()
    tracker(maze, start_point, points_visited_bktracker, points_visited_sttracker)
    backtracker(maze, goal, points_visited_bktracker, points_visited_sttracker)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to solve the maze: {elapsed_time:.12f} seconds")
else:
    print("The maze cannot be traversed from the start to the goal.")