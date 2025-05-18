from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}  
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, row_offset, column_offset):
        self.row_offset += row_offset
        self.column_offset += column_offset

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            moved_position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(moved_position)
        return moved_tiles

    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def undo_rotation(self):
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            x = offset_x + tile.column * self.cell_size
            y = offset_y + tile.row * self.cell_size
            tile_rect = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
