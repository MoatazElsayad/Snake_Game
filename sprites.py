import pygame
import random
from config import *

class Snake:
    def __init__(self, color=GREEN):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, 0)
        self.last_direction = (0, 0)
        self.next_turns = []
        self.color = color
        self.score = 0
        self.alive = True
        self.grow_pending = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Determine the direction we should check against
        if self.next_turns:
            check_dir = self.next_turns[-1]
        elif self.direction != (0, 0):
             check_dir = self.direction
        else:
             check_dir = self.last_direction

        # Prevent 180 degree turns
        if (point[0] * -1, point[1] * -1) == check_dir:
            return
        
        # Don't queue the same direction twice
        if point == check_dir:
            return

        # Limit queue size to prevent input lag buildup
        if len(self.next_turns) < 3:
            self.next_turns.append(point)

    def move(self):
        if self.next_turns:
            self.direction = self.next_turns.pop(0)
            self.last_direction = self.direction

        if self.direction == (0, 0):
            return

        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))

        # Check Boundaries
        if new[0] < 0 or new[0] >= SCREEN_WIDTH or new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            self.alive = False
            return

        # Check Self Collision
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.alive = False
            return

        self.positions.insert(0, new)
        if self.grow_pending > 0:
            self.grow_pending -= 1
            self.length += 1
        else:
            self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, 0)
        self.last_direction = (0, 0)
        self.next_turns = []
        self.score = 0
        self.alive = True
        self.grow_pending = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK if self.color != BLACK else WHITE, r, 1) # Border

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.turn((0, -1))
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.turn((0, 1))
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.turn((-1, 0))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn((1, 0))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)
