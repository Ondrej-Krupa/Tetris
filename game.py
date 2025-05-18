from grid import Grid
from blocks import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [
            LBlock(), JBlock(), TBlock(),
            SBlock(), ZBlock(), OBlock(), IBlock()
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, move_down_points=0):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 1000
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [
                LBlock(), JBlock(), TBlock(),
                SBlock(), ZBlock(), OBlock(), IBlock()
            ]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        for position in self.current_block.get_cell_positions():
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [
            LBlock(), JBlock(), TBlock(),
            SBlock(), ZBlock(), OBlock(), IBlock()
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False

    def block_fits(self):
        for tile in self.current_block.get_cell_positions():
            if not self.grid.is_inside(tile.row, tile.column) or not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()

    def block_inside(self):
        for tile in self.current_block.get_cell_positions():
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        next_block_x = 270
        next_block_y = 260

        if isinstance(self.next_block, IBlock):
            self.next_block.draw(screen, next_block_x - 15, next_block_y)
        elif isinstance(self.next_block, OBlock):
            self.next_block.draw(screen, next_block_x - 5, next_block_y + 20)
        else:
            self.next_block.draw(screen, next_block_x, next_block_y)
