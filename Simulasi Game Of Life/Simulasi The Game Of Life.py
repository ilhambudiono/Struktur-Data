import time
import os
import copy

ROWS = 10
COLS = 10

def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Pola awal (Glider)
    grid[1][2] = 1
    grid[2][3] = 1
    grid[3][1] = 1
    grid[3][2] = 1
    grid[3][3] = 1
    return grid

def print_grid(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        for cell in row:
            print("⬜" if cell == 0 else "⬛", end=" ")
        print()
    print("\nTekan Ctrl+C untuk berhenti")

def count_neighbors(grid, r, c):
    directions = [-1, 0, 1]
    count = 0
    for dr in directions:
        for dc in directions:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                count += grid[nr][nc]
    return count

def update_grid(grid):
    new_grid = copy.deepcopy(grid)
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = count_neighbors(grid, r, c)

            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def main():
    grid = create_grid()

    try:
        while True:
            print_grid(grid)
            grid = update_grid(grid)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulasi dihentikan.")

if __name__ == "__main__":
    main()
