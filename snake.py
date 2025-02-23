import pygame as pg
from constants import *
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NO_MOVEMENT = (0, 0)

class Snake:
    def __init__(self):
        self.body = [HEAD_POS, (HEAD_POS[0] + 1, HEAD_POS[1])]
        self.occupied_positions = {HEAD_POS}
        self.direction = Direction.NO_MOVEMENT
        self.color = (0, 255, 0) # Green Snake

    def is_valid_direction_change(self, new_direction):
        dx1, dy1 = self.direction.value
        dx2, dy2 = new_direction.value

        return (dx1 + dx2, dy1 + dy2) != (0, 0)
    
    def update_position(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        self.occupied_positions.add(new_head)

        tail = self.body.pop()
        self.occupied_positions.discard(tail)
    
    def check_collide_wall(self):
        head_x, head_y = self.body[0]
        if not -1 < head_x < 40:
            return True
        if not -1 < head_y < 30:
            return True
        return False 
    
    def check_collide_self(self):
        head_x, head_y = self.body[0]
        for i in range(1, len(self.body)):
            if self.body[i][0] == head_x and self.body[i][1] == head_y:
                return True
        return False
    
    def check_collide_food(self, food_pos):
        head_x, head_y = self.body[0]
        if head_x == food_pos[0] and head_y == food_pos[1]:
            return True
        return False

    def check_for_collision(self, food_pos):
        # If snake has collided with the 4 walls, or with itself return -1
        # If snake has collided with the food, return 1
        if self.check_collide_wall() or self.check_collide_self():
            return -1
        if self.check_collide_food(food_pos):
            # extend length
            self.extend_length()
            return 1

    def extend_length(self):
        self.body.extend([self.body[-1]] * 4)

    def draw(self, screen):
        for x, y in self.body:
            pg.draw.rect(
                screen,
                self.color,
                (x * 20, y * 20, 20, 20) # Convert grid position to pixel coordinates
            )

            pg.draw.rect(
                screen,
                (0, 0, 0),
                (x * 20, y * 20, 20, 20),
                1
            )