from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}  # rotation states -> list of Position
        self.cell_size = 30
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()
        self.position = Position(0, 3)  # výchozí pozice bloku ve hře

    def draw(self, screen):
        tiles = self.cells[self.rotation_state]
        for tile in tiles:
            x = (tile.column + self.position.column) * self.cell_size
            y = (tile.row + self.position.row) * self.cell_size
            tile_rect = pygame.Rect(x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
