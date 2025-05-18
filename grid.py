import pygame
from colors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for u in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()

    def is_inside(self, row, column):
        return 0 <= row < self.num_rows and 0 <= column < self.num_cols

    def is_empty(self, row, column):
        return self.grid[row][column] == 0

    def is_row_full(self, row):  
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, -1, -1):  
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed  
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell = self.grid[row][col]
                cell_rect = pygame.Rect(
                    col * self.cell_size + 11,
                    row * self.cell_size + 11,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                pygame.draw.rect(screen, self.colors[cell], cell_rect)
