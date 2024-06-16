import pygame
import random

pygame.init()

# Screen settings
screen_width = 300
screen_height = 600
block_size = 30
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# Colors
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128)
]

# Tetrimino shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

# Initialize grid
grid = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]
class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = (screen_width // block_size) // 2 - len(shape[0]) // 2
        self.y = 0

def create_tetrimino():
    shape = random.choice(shapes)
    color = colors[shapes.index(shape) + 1]
    return Tetrimino(shape, color)

def draw_grid():
    for y in range(screen_height // block_size):
        for x in range(screen_width // block_size):
            pygame.draw.rect(screen, (128, 128, 128), (x * block_size, y * block_size, block_size, block_size), 1)

def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, (tetrimino.x * block_size + x * block_size, tetrimino.y * block_size + y * block_size, block_size, block_size))

def draw_grid_blocks():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * block_size, y * block_size, block_size, block_size))

def check_collision(tetrimino, dx=0, dy=0):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetrimino.x + x + dx
                new_y = tetrimino.y + y + dy
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid) or grid[new_y][new_x]:
                    return True
    return False

def place_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetrimino.y + y][tetrimino.x + x] = tetrimino.color
    clear_lines()

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(new_grid) < len(grid):
        new_grid.insert(0, [0 for _ in range(len(grid[0]))])
    grid = new_grid


def main():
    clock = pygame.time.Clock()
    tetrimino = create_tetrimino()
    game_over = False
    fall_time = 0

    while not game_over:
        screen.fill((0, 0, 0))
        draw_grid()
        draw_grid_blocks()
        draw_tetrimino(tetrimino)
        pygame.display.flip()

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > 0.5:
            fall_time = 0
            if not check_collision(tetrimino, dy=1):
                tetrimino.y += 1
            else:
                place_tetrimino(tetrimino)
                tetrimino = create_tetrimino()
                if check_collision(tetrimino):
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(tetrimino, dx=-1):
                    tetrimino.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(tetrimino, dx=1):
                    tetrimino.x += 1
                if event.key == pygame.K_DOWN and not check_collision(tetrimino, dy=1):
                    tetrimino.y += 1
                if event.key == pygame.K_UP:
                    tetrimino.shape = list(zip(*tetrimino.shape[::-1]))
                    if check_collision(tetrimino):
                        tetrimino.shape = list(zip(*tetrimino.shape))[::-1]  # Revert rotation if collision occurs

if __name__ == "__main__":
    main()