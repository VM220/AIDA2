import numpy as np

# Define the goal state
GOAL_STATE = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
])

# Helper functions
def misplaced_tiles(state):
    """Heuristic: Counts the number of misplaced tiles compared to the goal."""
    return np.sum(state != GOAL_STATE) - 1  # -1 to exclude the blank tile

def manhattan_distance(state):
    """Heuristic: Calculates Manhattan distance of tiles from goal positions."""
    distance = 0
    for x in range(3):
        for y in range(3):
            value = state[x, y]
            if value != 0:
                goal_x, goal_y = divmod(value - 1, 3)
                distance += abs(x - goal_x) + abs(y - goal_y)
    return distance

def get_possible_moves(state):
    """Returns possible moves and resulting states from the current state."""
    moves = []
    x, y = np.argwhere(state == 0)[0]  # Locate the blank space (0)
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    
    for direction, (dx, dy) in directions.items():
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = state.copy()
            new_state[x, y], new_state[new_x, new_y] = new_state[new_x, new_y], new_state[x, y]
            moves.append((new_state, direction))
    
    return moves

def hill_climbing(initial_state, heuristic=misplaced_tiles):
    """Hill Climbing algorithm to solve the 8 Puzzle problem."""
    current_state = initial_state
    steps = 0

    while not np.array_equal(current_state, GOAL_STATE):
        neighbors = get_possible_moves(current_state)
        current_heuristic = heuristic(current_state)
        
        # Choose the best move based on the heuristic
        next_state = current_state
        next_heuristic = current_heuristic
        
        for state, direction in neighbors:
            h = heuristic(state)
            if h < next_heuristic:
                next_state, next_heuristic = state, h
        
        # If no better neighbor is found, return as a local maximum or plateau
        if next_heuristic >= current_heuristic:
            print("Stuck at a local maximum or plateau.")
            return current_state, steps, False  # Failure

        # Move to the next state
        current_state = next_state
        steps += 1
        print(f"Step {steps}: Current heuristic = {next_heuristic}")
        print(current_state)

    print("Goal state reached!")
    return current_state, steps, True  # Success

# Example of initial state
initial_state = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
])

# Solve the 8 Puzzle with Hill Climbing using Manhattan Distance heuristic
final_state, total_steps, success = hill_climbing(initial_state, heuristic=manhattan_distance)

if success:
    print(f"Solution found in {total_steps} steps!")
else:
    print("Failed to find a solution.")
