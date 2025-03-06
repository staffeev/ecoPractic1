import pygame
import numpy as np
import random

# Определение параметров
CELL_SIZE = 10  # Размер клетки
GRID_SIZE = (80, 60)  # Размер сетки (ширина, высота)
WIDTH, HEIGHT = GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE
FPS = 2  # Замедленная игра

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Эволюция животных")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 14)  # Шрифт для текста

# Загрузка фонового изображения
background = pygame.image.load("background.png")  # Укажите путь к вашему изображению
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def generate_grid(size):
    return np.zeros(size, dtype=int)

def draw_grid(surface, grid):
    surface.blit(background, (0, 0))  # Отрисовка фона
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            if grid[x, y] > 0:
                pygame.draw.rect(surface, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                text = font.render(str(grid[x, y]), True, WHITE)
                surface.blit(text, (x * CELL_SIZE + 2, y * CELL_SIZE + 2))

def count_neighbors(grid, x, y):
    neighbors = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Только горизонтальные и вертикальные соседи
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE[0] and 0 <= ny < GRID_SIZE[1]:
            neighbors += grid[nx, ny]
    return neighbors

def update_grid(grid):
    new_grid = grid.copy()
    for x in range(GRID_SIZE[0]):
        for y in range(GRID_SIZE[1]):
            if grid[x, y] > 0:
                # Увеличиваем население клетки
                new_grid[x, y] += 1
                
                # Чем больше животных, тем выше шанс заражения соседних клеток
                infection_chance = min(0.1 * new_grid[x, y], 0.5)  # Максимальный шанс заражения 50%
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE[0] and 0 <= ny < GRID_SIZE[1] and new_grid[nx, ny] == 0:
                        if random.random() < infection_chance:
                            new_grid[nx, ny] = 1  # Заражаем соседнюю клетку
    return new_grid

grid = generate_grid(GRID_SIZE)
running = True
simulating = False
next_step = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
            elif event.key == pygame.K_r:
                grid = generate_grid(GRID_SIZE)
            elif event.key == pygame.K_c:
                grid = np.random.choice([0, 1], size=GRID_SIZE, p=[0.8, 0.2])
            elif event.key == pygame.K_RIGHT:  # Один шаг вперед
                next_step = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid[x // CELL_SIZE, y // CELL_SIZE] = 1  # Населяем клетку
    
    if simulating or next_step:
        grid = update_grid(grid)
        next_step = False
    
    draw_grid(screen, grid)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
