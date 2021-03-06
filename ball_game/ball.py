from __future__ import annotations

import pygame as pg
from pygame.math import Vector2 as Vector
from typing import Optional, NamedTuple
from itertools import combinations
import random

from .settings import FPS, GRAVITY, HEIGHT, WIDTH, SPEED_MULTIPLIER, COLOURS, BALL_COLOURS, ENERGY_LOSS

class Coordinates(NamedTuple):
    x: int
    y: int

class Ball:
    def __init__(self, x: int, y: int, radius: int, screen: pg.surface.Surface, colour: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.start = Coordinates(self.x, self.y)
        self.radius = radius
        self.screen = screen
        self.colour = colour

        self.down = Vector(0, 1) * SPEED_MULTIPLIER
        self.up = Vector(0, -1) * SPEED_MULTIPLIER
        self.left = Vector(-1, 0) * SPEED_MULTIPLIER
        self.right = Vector(1, 0) * SPEED_MULTIPLIER
        self.null_position = Vector(0, 0)

        self.current_direction: Vector = self.down

        self.dy = 1
        self.dx = 0.25
        
    def __repr__(self) -> str:
        return f'Ball(x={self.x}, y={self.y}, radius={self.radius}, colour={self.colour})'
    
    def draw_circle(self) -> None:
        pg.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius)
    
    def update(self):
        self.y += self.dy
        self.x += self.dx
        self.dy += GRAVITY

        if self.y >= (HEIGHT - self.radius):
            self.dy = (-self.dy * ENERGY_LOSS)
            self.y = HEIGHT - self.radius
        
        if self.x >= (WIDTH - self.radius) or self.x <= self.radius:
            self.dx = -self.dx

    
    def collision(self, ball: Ball) -> bool:
        """Checks if two balls have collided
        uses a^2 + b^2 = c^2 and checks if the distance between
        the two centres is less than the sum of the two radiuses"""
        return ((self.x - ball.x) ** 2) + ((self.y - ball.y) ** 2) < ((self.radius + ball.radius) ** 2)
    
class Player(Ball):...        

class BallContainer:
    def __init__(self, *balls: Ball, container:Optional[list[Ball]] = None) -> None:
        self.container = container if container is not None else []
        self.container.extend(balls)
    
    def __repr__(self) -> str:
        return f'BallContainer({self.container})'
    
    def draw_balls(self) -> None:
        for ball in self.container:
            ball.draw_circle()
    
    def add_ball(self, ball: Ball) -> None:
        self.container.append(ball)
    
    def remove_ball(self, *balls: Ball) -> None:
        for ball in balls:
            self.container.remove(ball)
    
    def update(self) -> bool:
        hits = self.detect_collisions()
        for ball in self.container:
            ball.update()
        return any(hits)
    
    def reset_container(self) -> None:
        self.container = []
    
    def detect_collisions(self) -> list[bool]:
        hits = []
        for b1, b2 in combinations(self.container, 2):
            if b1 is b2:
                continue
            
            if b1.collision(b2):
                if self.combine_or_destroy(b1, b2):
                    args: tuple[int, int, int, pg.surface.Surface, tuple[int, int, int]] = ((b1.x + b2.x) // 2, (b1.y + b2.y) // 2, b1.radius + b2.radius, b1.screen, COLOURS['yellow'])
                    self.add_ball(Ball(*args))
                try:
                    self.remove_ball(b1, b2)
                except ValueError:
                    pass
                hits.append(True)
            else:
                hits.append(False)
        return hits
    
    def combine_or_destroy(self, b1: Ball, b2: Ball) -> bool:
        """Generate a boolean depending on the balls colour
        combine = True
        destroy = False"""
        return bool(random.randbytes(1))

                    